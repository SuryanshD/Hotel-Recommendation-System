from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib import messages
from django.db.models import Q, Avg, Count, Min
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from .models import Hotel, Room, Booking, Review, UserInteraction, SearchHistory
from .forms import HotelSearchForm, BookingForm, ReviewForm, HotelFilterForm
from .services.recommendation import recommendation_service
from accounts.models import UserPreference


class HotelListView(ListView):
    """
    HotelListView displays a paginated list of active hotels with advanced filtering, sorting, and recommendation features.
    Features:
    - Filters hotels by city, area, check-in/check-out dates, number of guests, price range, hotel type, star rating, and amenities.
    - Supports sorting by rating, price (low to high, high to low), and hotel name.
    - Persists user search history if authenticated.
    - Provides hotel recommendations for authenticated users based on search criteria.
    - Integrates search and filter forms into the context for template rendering.
    Context:
    - 'hotels': Paginated queryset of filtered hotels.
    - 'search_form': Instance of HotelSearchForm pre-filled with GET data.
    - 'filter_form': Instance of HotelFilterForm pre-filled with GET data.
    - 'recommended_hotels': List of recommended hotels (for authenticated users).
    Pagination:
    - 12 hotels per page.
    Usage:
    - Intended for use as a Django ListView for hotel listings with rich filtering and personalization.
    """

    model = Hotel
    template_name = "booking/hotel_list.html"
    context_object_name = "hotels"
    paginate_by = 12

    def get_queryset(self):
        queryset = Hotel.objects.filter(is_active=True)

        city = self.request.GET.get("city")
        area = self.request.GET.get("area")
        check_in = self.request.GET.get("check_in_date")
        check_out = self.request.GET.get("check_out_date")
        guests = self.request.GET.get("guests", 2)
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if city:
            queryset = queryset.filter(city__icontains=city)
        if area:
            queryset = queryset.filter(area__icontains=area)

        if check_in and check_out and guests:
            try:
                guests = int(guests)
                queryset = queryset.filter(
                    rooms__capacity__gte=guests, rooms__is_available=True
                ).distinct()
            except ValueError:
                pass

        if min_price:
            try:
                queryset = queryset.filter(
                    rooms__price_per_night__gte=Decimal(min_price)
                )
            except (ValueError, TypeError):
                pass

        if max_price:
            try:
                queryset = queryset.filter(
                    rooms__price_per_night__lte=Decimal(max_price)
                )
            except (ValueError, TypeError):
                pass

        filter_form = HotelFilterForm(self.request.GET)
        if filter_form.is_valid():
            hotel_type = filter_form.cleaned_data.get("hotel_type")
            star_rating = filter_form.cleaned_data.get("star_rating")
            amenities = filter_form.cleaned_data.get("amenities")
            sort_by = filter_form.cleaned_data.get("sort_by", "rating")

            if hotel_type:
                queryset = queryset.filter(hotel_type=hotel_type)

            if star_rating:
                queryset = queryset.filter(average_rating__gte=int(star_rating))

            if amenities:
                for amenity in amenities:
                    queryset = queryset.filter(amenities__icontains=amenity)

            if sort_by == "rating":
                queryset = queryset.order_by("-average_rating", "-total_reviews")
            elif sort_by == "price_low":
                queryset = queryset.annotate(
                    room_min_price=Min("rooms__price_per_night")
                ).order_by("room_min_price")
            elif sort_by == "price_high":
                queryset = queryset.annotate(
                    room_min_price=Min("rooms__price_per_night")
                ).order_by("-room_min_price")
            elif sort_by == "name":
                queryset = queryset.order_by("name")

        if self.request.user.is_authenticated and city:
            try:
                SearchHistory.objects.create(
                    user=self.request.user,
                    city=city,
                    area=area or "",
                    check_in_date=check_in or date.today(),
                    check_out_date=check_out or (date.today() + timedelta(days=1)),
                    guests=int(guests) if guests else 2,
                    min_price=Decimal(min_price) if min_price else None,
                    max_price=Decimal(max_price) if max_price else None,
                )
            except:
                pass

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = HotelSearchForm(self.request.GET)
        context["filter_form"] = HotelFilterForm(self.request.GET)

        if self.request.user.is_authenticated:
            city = self.request.GET.get("city")
            area = self.request.GET.get("area")
            check_in = self.request.GET.get("check_in_date")
            check_out = self.request.GET.get("check_out_date")
            guests = int(self.request.GET.get("guests", 2))

            recommended_hotels = recommendation_service.get_recommendations(
                user=self.request.user,
                city=city,
                area=area,
                check_in_date=check_in,
                check_out_date=check_out,
                guests=guests,
                limit=6,
            )
            context["recommended_hotels"] = recommended_hotels

        return context


class HotelDetailView(DetailView):
    """
    Displays detailed information about a specific hotel, including available rooms, recent reviews, and similar hotel recommendations.
    Attributes:
        model (Hotel): The Hotel model to retrieve details for.
        template_name (str): The template used to render the hotel detail page.
        context_object_name (str): The context variable name for the hotel object.
    Methods:
        get_context_data(**kwargs):
            Extends the context with:
                - Available rooms for the hotel.
                - The latest 10 reviews and a review form.
                - Search parameters (check-in date, check-out date, guests) from GET request.
                - Tracks user interaction if the user is authenticated.
                - Provides a list of similar hotels, excluding the current hotel.
    """

    model = Hotel
    template_name = "booking/hotel_detail.html"
    context_object_name = "hotel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel = self.get_object()

        context["rooms"] = hotel.rooms.filter(is_available=True)
        context["reviews"] = hotel.reviews.all()[:10]
        context["review_form"] = ReviewForm()
        context["check_in_date"] = self.request.GET.get("check_in_date")
        context["check_out_date"] = self.request.GET.get("check_out_date")
        context["guests"] = self.request.GET.get("guests", 2)

        if self.request.user.is_authenticated:
            UserInteraction.objects.create(
                user=self.request.user, hotel=hotel, interaction_type="view", weight=1.0
            )

        similar_hotels = recommendation_service.get_recommendations(
            user=self.request.user if self.request.user.is_authenticated else None,
            city=hotel.city,
            area=hotel.area,
            limit=4,
        )
        context["similar_hotels"] = [h for h in similar_hotels if h.id != hotel.id][:3]
        return context


class BookingCreateView(LoginRequiredMixin, View):
    """
    View for creating a new booking for a specific hotel room.
    This view handles both GET and POST requests:
    - GET: Renders the booking creation form, pre-filling it with search parameters from the query string.
    - POST: Processes the submitted booking form, validates the data, calculates the total amount based on the number of nights and room price, saves the booking, logs the user interaction, and redirects to the booking detail page upon success.
    Attributes:
        template_name (str): The template used to render the booking creation form.
    Methods:
        get(request, hotel_id, room_id):
            Handles GET requests. Retrieves the specified hotel and room, initializes the booking form with any provided search parameters, and renders the form.
        post(request, hotel_id, room_id):
            Handles POST requests. Validates and processes the submitted booking form, calculates the total amount, saves the booking, logs the user interaction, and redirects to the booking detail page if successful. If the form is invalid, re-renders the form with errors.
    """

    template_name = "booking/booking_create.html"

    def get(self, request, hotel_id, room_id):
        hotel = get_object_or_404(Hotel, id=hotel_id, is_active=True)
        room = get_object_or_404(Room, id=room_id, hotel=hotel, is_available=True)

        # Pre-fill form with search parameters
        initial_data = {
            "check_in_date": request.GET.get("check_in_date"),
            "check_out_date": request.GET.get("check_out_date"),
            "guests": request.GET.get("guests", 2),
        }

        form = BookingForm(initial=initial_data, room=room)

        context = {
            "hotel": hotel,
            "room": room,
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request, hotel_id, room_id):
        hotel = get_object_or_404(Hotel, id=hotel_id, is_active=True)
        room = get_object_or_404(Room, id=room_id, hotel=hotel, is_available=True)

        form = BookingForm(request.POST, room=room)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.hotel = hotel
            booking.room = room

            # Calculate total amount
            nights = (booking.check_out_date - booking.check_in_date).days
            booking.total_amount = room.price_per_night * nights

            booking.save()

            UserInteraction.objects.create(
                user=request.user, hotel=hotel, interaction_type="book", weight=5.0
            )

            messages.success(
                request, f"Booking confirmed! Reference: {booking.booking_reference}"
            )
            return redirect("booking:booking_detail", booking_id=booking.id)

        context = {
            "hotel": hotel,
            "room": room,
            "form": form,
        }
        return render(request, self.template_name, context)


class BookingDetailView(LoginRequiredMixin, DetailView):
    """
    BookingDetailView displays the details of a single Booking instance for the currently authenticated user.
    Methods:
        get_queryset(self):
            Returns a queryset of Booking objects filtered by the current user, ensuring users can only access their own bookings.
    """

    model = Booking
    template_name = "booking/booking_detail.html"
    context_object_name = "booking"
    pk_url_kwarg = "booking_id"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingHistoryView(LoginRequiredMixin, ListView):
    """
    View to display the booking history for the currently logged-in user.
    Methods:
        get_queryset(self):
            Returns a queryset of Booking objects filtered by the current user,
            ordered by creation date in descending order.
    """

    model = Booking
    template_name = "booking/booking_history.html"
    context_object_name = "bookings"
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by("-created_at")


class ReviewCreateView(LoginRequiredMixin, View):
    """
    View to handle the creation of hotel reviews by authenticated users.
    POST:
        - Checks if the user has already reviewed the specified hotel.
        - If not, validates and saves the submitted review form.
        - Associates the review with the user, hotel, and (if available) a related booking.
        - Records a user interaction for recommendation or analytics purposes.
        - Provides feedback messages for success or form errors.
        - Redirects to the hotel detail page after processing.
    Args:
        request (HttpRequest): The HTTP request object.
        hotel_id (int): The primary key of the hotel being reviewed.
    Returns:
        HttpResponseRedirect: Redirects to the hotel detail page with appropriate messages.
    """

    def post(self, request, hotel_id):
        hotel = get_object_or_404(Hotel, id=hotel_id)

        if Review.objects.filter(user=request.user, hotel=hotel).exists():
            messages.error(request, "You have already reviewed this hotel.")
            return redirect("booking:hotel_detail", pk=hotel_id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.hotel = hotel
            booking = Booking.objects.filter(
                user=request.user,
                hotel=hotel,
                booking_status__in=["checked_out", "confirmed"],
            ).first()
            if booking:
                review.booking = booking

            review.save()

            UserInteraction.objects.create(
                user=request.user, hotel=hotel, interaction_type="review", weight=3.0
            )

            messages.success(request, "Thank you for your review!")
        else:
            messages.error(request, "Please correct the errors in your review.")

        return redirect("booking:hotel_detail", pk=hotel_id)


class HotelSearchView(View):
    """
    HotelSearchView handles hotel search form display and submission.
    GET:
        - Renders the hotel search form for user input.
    POST:
        - Validates the submitted search form.
        - If valid, redirects to the hotel list page with search parameters as query string.
        - If invalid, re-renders the form with validation errors.
    Attributes:
        template_name (str): Path to the hotel search template.
    Methods:
        get(request):
            Handles GET requests to display the search form.
        post(request):
            Handles POST requests to process the search form and redirect with search parameters.
    """

    template_name = "booking/hotel_search.html"

    def get(self, request):
        form = HotelSearchForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = HotelSearchForm(request.POST)
        if form.is_valid():
            # Redirect to hotel list with search parameters
            params = {
                "city": form.cleaned_data["city"],
                "area": form.cleaned_data.get("area", ""),
                "check_in_date": form.cleaned_data["check_in_date"],
                "check_out_date": form.cleaned_data["check_out_date"],
                "guests": form.cleaned_data["guests"],
            }

            if form.cleaned_data.get("min_price"):
                params["min_price"] = form.cleaned_data["min_price"]
            if form.cleaned_data.get("max_price"):
                params["max_price"] = form.cleaned_data["max_price"]

            # Build query string
            query_string = "&".join([f"{k}={v}" for k, v in params.items() if v])
            return redirect(f"/booking/hotels/?{query_string}")

        return render(request, self.template_name, {"form": form})


@login_required
def cancel_booking(request, booking_id):
    """
    View to handle the cancellation of a booking by the logged-in user.
    Args:
        request (HttpRequest): The HTTP request object.
        booking_id (int): The ID of the booking to be cancelled.
    Behavior:
        - Retrieves the booking for the current user by ID.
        - Prevents cancellation if the booking is already cancelled or checked out.
        - Disallows cancellation within 24 hours of the check-in date.
        - On POST request, updates the booking status to 'cancelled' and redirects to booking history.
        - On GET request, renders the cancellation confirmation page.
    Returns:
        HttpResponse: Redirects to booking detail or booking history, or renders the cancellation page.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.booking_status in ["cancelled", "checked_out"]:
        messages.error(request, "This booking cannot be cancelled.")
        return redirect("booking:booking_detail", booking_id=booking_id)

    # Check if cancellation is allowed (e.g., at least 24 hours before check-in)
    if booking.check_in_date <= date.today() + timedelta(days=1):
        messages.error(
            request, "Cancellation is not allowed within 24 hours of check-in."
        )
        return redirect("booking:booking_detail", booking_id=booking_id)

    if request.method == "POST":
        booking.booking_status = "cancelled"
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
        return redirect("booking:booking_history")

    return render(request, "booking/cancel_booking.html", {"booking": booking})


def ajax_room_availability(request):
    """AJAX endpoint to check room availability"""
    if request.method == "GET":
        room_id = request.GET.get("room_id")
        check_in = request.GET.get("check_in_date")
        check_out = request.GET.get("check_out_date")

        if not all([room_id, check_in, check_out]):
            return JsonResponse({"available": False, "error": "Missing parameters"})

        try:
            room = Room.objects.get(id=room_id, is_available=True)

            # Check for conflicting bookings
            conflicting_bookings = Booking.objects.filter(
                room=room,
                booking_status__in=["confirmed", "checked_in"],
                check_in_date__lt=check_out,
                check_out_date__gt=check_in,
            ).exists()

            if conflicting_bookings:
                return JsonResponse(
                    {
                        "available": False,
                        "message": "Room not available for selected dates",
                    }
                )

            # Calculate total price
            from datetime import datetime

            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
            nights = (check_out_date - check_in_date).days
            total_price = room.price_per_night * nights

            return JsonResponse(
                {
                    "available": True,
                    "nights": nights,
                    "price_per_night": str(room.price_per_night),
                    "total_price": str(total_price),
                }
            )

        except Room.DoesNotExist:
            return JsonResponse({"available": False, "error": "Room not found"})
        except Exception as e:
            return JsonResponse({"available": False, "error": str(e)})

    return JsonResponse({"available": False, "error": "Invalid request method"})


class RecommendedHotelsView(LoginRequiredMixin, View):
    """View to get personalized hotel recommendations"""

    def get(self, request):
        city = request.GET.get("city")
        area = request.GET.get("area")
        limit = int(request.GET.get("limit", 10))

        recommended_hotels = recommendation_service.get_recommendations(
            user=request.user, city=city, area=area, limit=limit
        )

        context = {"hotels": recommended_hotels, "title": "Recommended for You"}
        return render(request, "booking/recommended_hotels.html", context)
