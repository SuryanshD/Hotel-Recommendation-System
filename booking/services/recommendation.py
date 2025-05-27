import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from django.db.models import Q, Avg, Count
from django.contrib.auth.models import User
from ..models import Hotel, UserInteraction, Booking, Review, SearchHistory
from accounts.models import UserPreference
import logging

logger = logging.getLogger(__name__)


class HotelRecommendationService:
    """
    HotelRecommendationService provides hotel recommendations using a hybrid approach that combines content-based filtering, collaborative filtering, and location-based filtering.
    Methods
    -------
    __init__():
        Initializes the service with TF-IDF vectorizer, KNN model, and SVD model.
    get_recommendations(user=None, city=None, area=None, check_in_date=None, check_out_date=None, guests=1, limit=10):
        Returns a list of recommended hotels based on user authentication, preferences, and search parameters.
    _get_personalized_recommendations(user, hotels, city, area, check_in_date, check_out_date, guests, limit):
        Generates personalized hotel recommendations for authenticated users by combining content-based, collaborative, and location-based scores.
    _content_based_filtering(user, hotels, user_preference, city, area, guests):
        Computes similarity scores between user profile and hotels using TF-IDF and cosine similarity.
    _collaborative_filtering(user, hotels):
        Predicts user-hotel ratings using collaborative filtering (SVD) based on user interactions and reviews.
    _location_based_filtering(user, hotels, city, area):
        Scores hotels based on similarity between user location preferences and hotel locations using TF-IDF and KNN.
    _create_user_profile(user, user_preference):
        Constructs a textual user profile from preferences, booking history, and reviews for content-based filtering.
    _get_general_recommendations(hotels, city, area, check_in_date, check_out_date, guests, limit):
        Returns general hotel recommendations for non-authenticated users, sorted by rating and popularity.
    """

    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
        self.knn_model = NearestNeighbors(n_neighbors=10, metric="cosine")
        self.svd_model = SVD()

    def get_recommendations(
        self,
        user=None,
        city=None,
        area=None,
        check_in_date=None,
        check_out_date=None,
        guests=1,
        limit=10,
    ):
        """
        Get hotel recommendations using hybrid approach
        """
        try:
            # Get base hotels
            hotels = Hotel.objects.filter(is_active=True)

            if city:
                hotels = hotels.filter(city__icontains=city)
            if area:
                hotels = hotels.filter(area__icontains=area)

            if not hotels.exists():
                return hotels.none()

            # If user is authenticated, use personalized recommendations
            if user and user.is_authenticated:
                return self._get_personalized_recommendations(
                    user,
                    hotels,
                    city,
                    area,
                    check_in_date,
                    check_out_date,
                    guests,
                    limit,
                )
            else:
                return self._get_general_recommendations(
                    hotels, city, area, check_in_date, check_out_date, guests, limit
                )

        except Exception as e:
            logger.error(f"Error in get_recommendations: {str(e)}")
            return Hotel.objects.filter(is_active=True)[:limit]

    def _get_personalized_recommendations(
        self, user, hotels, city, area, check_in_date, check_out_date, guests, limit
    ):
        """
        Get personalized recommendations using hybrid filtering
        """
        try:
            # Get user preferences
            user_preference = getattr(user, "userpreference", None)

            # 1. Content-based filtering
            content_scores = self._content_based_filtering(
                user, hotels, user_preference, city, area, guests
            )

            # 2. Collaborative filtering
            collaborative_scores = self._collaborative_filtering(user, hotels)

            # 3. Location-based filtering
            location_scores = self._location_based_filtering(user, hotels, city, area)

            # 4. Combine scores with weights
            final_scores = {}
            for hotel_id in hotels.values_list("id", flat=True):
                content_score = content_scores.get(hotel_id, 0)
                collaborative_score = collaborative_scores.get(hotel_id, 0)
                location_score = location_scores.get(hotel_id, 0)

                # Weighted combination
                final_score = (
                    0.4 * content_score
                    + 0.35 * collaborative_score
                    + 0.25 * location_score
                )
                final_scores[hotel_id] = final_score

            # Sort by final scores
            sorted_hotel_ids = sorted(
                final_scores.keys(), key=lambda x: final_scores[x], reverse=True
            )

            recommended_hotels = []
            for hotel_id in sorted_hotel_ids[:limit]:
                try:
                    hotel = hotels.get(id=hotel_id)
                    recommended_hotels.append(hotel)
                except Hotel.DoesNotExist:
                    continue

            return recommended_hotels

        except Exception as e:
            logger.error(f"Error in personalized recommendations: {str(e)}")
            return self._get_general_recommendations(
                hotels, city, area, check_in_date, check_out_date, guests, limit
            )

    def _content_based_filtering(
        self, user, hotels, user_preference, city, area, guests
    ):
        """
        Content-based filtering using TF-IDF and cosine similarity
        """
        try:
            scores = {}

            # Create user profile based on preferences and booking history
            user_profile = self._create_user_profile(user, user_preference)

            hotel_features = []
            hotel_ids = []
            for hotel in hotels:
                features = []
                features.append(hotel.city)
                features.append(hotel.area)
                features.append(hotel.hotel_type)
                features.extend(hotel.amenities or [])
                features.append(f"star_{hotel.average_rating}")
                features.append(f"rating_{int(hotel.average_rating)}")

                hotel_features.append(" ".join(features))
                hotel_ids.append(hotel.id)

            if not hotel_features:
                return scores

            all_features = hotel_features + [user_profile]
            # Calculate TF-IDF
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_features)
            # Calculate cosine similarity between user profile and hotels
            user_vector = tfidf_matrix[-1]  # Last item is user profile
            hotel_vectors = tfidf_matrix[:-1]  # All except last

            similarities = cosine_similarity(user_vector, hotel_vectors).flatten()

            # Create scores dictionary
            for i, hotel_id in enumerate(hotel_ids):
                scores[hotel_id] = similarities[i]

            return scores

        except Exception as e:
            logger.error(f"Error in content-based filtering: {str(e)}")
            return {}

    def _collaborative_filtering(self, user, hotels):
        """
        Collaborative filtering using SVD
        """
        try:
            scores = {}

            interactions = UserInteraction.objects.filter(hotel__in=hotels).values(
                "user_id", "hotel_id", "weight"
            )
            reviews = Review.objects.filter(hotel__in=hotels).values(
                "user_id", "hotel_id", "rating"
            )

            data = []
            for review in reviews:
                data.append(
                    {
                        "user_id": review["user_id"],
                        "hotel_id": review["hotel_id"],
                        "rating": review["rating"],
                    }
                )

            for interaction in interactions:
                rating = min(5, max(1, interaction["weight"] * 3))
                data.append(
                    {
                        "user_id": interaction["user_id"],
                        "hotel_id": interaction["hotel_id"],
                        "rating": rating,
                    }
                )

            if len(data) < 10:  # Not enough data for collaborative filtering
                return scores

            df = pd.DataFrame(data)
            reader = Reader(rating_scale=(1, 5))
            dataset = Dataset.load_from_df(
                df[["user_id", "hotel_id", "rating"]], reader
            )

            # Train SVD model
            trainset = dataset.build_full_trainset()
            self.svd_model.fit(trainset)

            # Get predictions for current user
            for hotel in hotels:
                try:
                    prediction = self.svd_model.predict(user.id, hotel.id)
                    scores[hotel.id] = prediction.est / 5.0  # Normalize to 0-1
                except:
                    scores[hotel.id] = 0.5  # Default score

            return scores

        except Exception as e:
            logger.error(f"Error in collaborative filtering: {str(e)}")
            return {}

    def _location_based_filtering(self, user, hotels, city, area):
        """
        Location-based filtering using KNN with TF-IDF
        """
        try:
            scores = {}

            # Get user's location preferences
            user_locations = []
            user_preference = getattr(user, "userpreference", None)
            if user_preference and user_preference.locations:
                user_locations.extend(user_preference.locations)

            recent_searches = SearchHistory.objects.filter(user=user)[:10]
            for search in recent_searches:
                user_locations.append(search.city)
                if search.area:
                    user_locations.append(search.area)

            recent_bookings = Booking.objects.filter(user=user)[:10]
            for booking in recent_bookings:
                user_locations.append(booking.hotel.city)
                user_locations.append(booking.hotel.area)

            if not user_locations:
                if city:
                    user_locations.append(city)
                if area:
                    user_locations.append(area)

            if not user_locations:
                return scores

            hotel_locations = []
            hotel_ids = []

            for hotel in hotels:
                location_text = f"{hotel.city} {hotel.area}"
                hotel_locations.append(location_text)
                hotel_ids.append(hotel.id)

            user_location_text = " ".join(user_locations)

            all_locations = hotel_locations + [user_location_text]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_locations)

            user_vector = tfidf_matrix[-1]
            hotel_vectors = tfidf_matrix[:-1]

            similarities = cosine_similarity(user_vector, hotel_vectors).flatten()

            for i, hotel_id in enumerate(hotel_ids):
                scores[hotel_id] = similarities[i]

            return scores

        except Exception as e:
            logger.error(f"Error in location-based filtering: {str(e)}")
            return {}

    def _create_user_profile(self, user, user_preference):
        """
        Create user profile text for content-based filtering
        """
        profile_features = []

        if user_preference:
            if user_preference.locations:
                profile_features.extend(user_preference.locations)
            if user_preference.amenities:
                profile_features.extend(user_preference.amenities)

        bookings = Booking.objects.filter(user=user).select_related("hotel")[:10]
        for booking in bookings:
            hotel = booking.hotel
            profile_features.append(hotel.city)
            profile_features.append(hotel.area)
            profile_features.append(hotel.hotel_type)
            if hotel.amenities:
                profile_features.extend(hotel.amenities)
            profile_features.append(f"star_{hotel.average_rating}")

        reviews = Review.objects.filter(user=user).select_related("hotel")[:10]
        for review in reviews:
            hotel = review.hotel
            if review.rating >= 4:
                profile_features.append(hotel.city)
                profile_features.append(hotel.hotel_type)
                if hotel.amenities:
                    profile_features.extend(hotel.amenities)

        return " ".join(profile_features) if profile_features else "default"

    def _get_general_recommendations(
        self, hotels, city, area, check_in_date, check_out_date, guests, limit
    ):
        """
        Get general recommendations for non-authenticated users
        """
        try:
            return hotels.annotate(
                booking_count=Count("bookings"), review_count=Count("reviews")
            ).order_by("-average_rating", "-booking_count", "-review_count", "name")[
                :limit
            ]

        except Exception as e:
            logger.error(f"Error in general recommendations: {str(e)}")
            return hotels[:limit]


recommendation_service = HotelRecommendationService()
