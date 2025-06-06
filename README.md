# Hotel Booking Recommendation System

A comprehensive hotel booking web application that allows users to search, view, and reserve hotel rooms online. The application features an advanced machine learning-powered recommendation engine that suggests hotels based on user preferences, past booking history, and collaborative filtering techniques.


## Features

### Core Booking Features
- *User Registration & Authentication*: Secure user accounts with profile management
- *Advanced Hotel Search*: Filter by location, dates, price range, amenities, and ratings
- *Detailed Hotel Information*: Comprehensive hotel details, high-quality photos, and user reviews
- *Reservation Management*: Book, modify, and cancel reservations with real-time availability
- *User Reviews & Ratings*: Rate and review hotels after stays

### Recommendation Engine Features
- *Personalized Hotel Recommendations*: ML-powered suggestions based on user behavior
- *Multiple Recommendation Algorithms*: Hybrid approach using various ML techniques
- *Real-time Recommendations*: Dynamic suggestions based on current search patterns
- *Similar Hotels Discovery*: Find hotels similar to ones you've liked

## Recommendation System

### Types of Recommendations

#### 1. *Collaborative Filtering*
Collaborative filtering works on the principle that users with similar preferences in the past will have similar preferences in the future. This approach analyzes user-item interactions to make recommendations.

*User-Based Collaborative Filtering*: This method identifies users who have similar booking patterns and preferences. If User A and User B have booked similar hotels and given similar ratings, the system will recommend hotels that User B liked to User A. The algorithm calculates similarity between users based on their rating patterns and booking history.

*Item-Based Collaborative Filtering*: Instead of finding similar users, this approach finds similar hotels. If a user liked Hotel X, the system recommends other hotels that are frequently liked by users who also liked Hotel X. This method is often more stable than user-based filtering as hotel characteristics change less frequently than user preferences.

*Matrix Factorization*: This advanced technique decomposes the user-hotel interaction matrix into lower-dimensional matrices that capture latent factors. These hidden factors might represent concepts like "luxury preference," "budget consciousness," or "location importance." The algorithm learns these factors automatically from the data.

#### 2. *Content-Based Filtering*
Content-based filtering recommends hotels based on the characteristics of hotels that a user has previously liked or booked. This approach analyzes hotel features and user preferences to make recommendations.

*Hotel Feature Analysis*: The system analyzes various hotel attributes such as amenities (pool, gym, spa), location type (city center, airport, beach), star rating, price range, and architectural style. It creates a profile of preferred hotel characteristics for each user based on their booking history.

*User Profile Matching*: The algorithm builds a comprehensive user profile that includes preferred amenities, typical price range, location preferences, and travel patterns. New hotel recommendations are generated by matching these preferences with available hotels.

*Similarity Scoring*: The system calculates how similar each hotel is to the user's preferred hotel characteristics using mathematical similarity measures. Hotels with higher similarity scores are more likely to be recommended.

#### 3. *Hybrid Recommendations*
Hybrid approaches combine multiple recommendation techniques to overcome the limitations of individual methods and provide more accurate and diverse recommendations.

*Weighted Combination*: This method combines collaborative and content-based filtering by assigning weights to each approach. For example, 60% weight might be given to collaborative filtering and 40% to content-based filtering, with the final recommendation score being a weighted average.

*Switching Hybrid*: The system intelligently switches between different algorithms based on the situation. For new users with limited data, it might rely more on content-based filtering, while for users with rich interaction history, collaborative filtering might be preferred.


#### 4. *Context-Aware Recommendations*
Context-aware systems consider situational factors that might influence user preferences at the time of booking.

*Location-Based Context*: Geographic factors play a crucial role. The system considers the user's current location, travel distance preferences, and regional popularity of hotels. It might recommend different types of accommodations for business trips versus leisure travel.


## Machine Learning Algorithms Explained

### Collaborative Filtering Algorithms

*Singular Value Decomposition (SVD)*: SVD is a matrix factorization technique that decomposes the user-hotel rating matrix into three matrices representing users, latent factors, and hotels. It identifies hidden patterns in user preferences and hotel characteristics. The algorithm is particularly effective at handling sparse data and can predict ratings for hotels that users haven't interacted with.

*SVD++ (Enhanced SVD)*: This is an extension of SVD that incorporates implicit feedback along with explicit ratings. While SVD only uses direct ratings, SVD++ also considers implicit signals like hotel views, search patterns, and booking attempts without completion. This provides a more comprehensive understanding of user preferences.

*Non-negative Matrix Factorization (NMF)*: NMF decomposes the rating matrix into non-negative factors, which often have more interpretable meanings. The non-negativity constraint ensures that the latent factors represent additive combinations of features, making the model more interpretable for business understanding.

*K-Nearest Neighbors (KNN) Variants*: 
- *KNNBasic*: Finds the most similar users or hotels based on rating patterns and makes predictions based on their preferences.
- *KNNWithMeans*: Adjusts for user or hotel rating biases by considering average ratings.
- *KNNWithZScore*: Normalizes ratings using z-scores to account for different rating scales used by different users.

*Baseline Algorithms*: These establish baseline predictions by considering global average ratings, user rating tendencies, and hotel rating tendencies. They serve as a foundation that other algorithms can build upon.

*Co-Clustering*: This algorithm simultaneously clusters users and hotels into groups, assuming that users in the same cluster have similar preferences for hotels in specific hotel clusters. It's particularly useful for identifying market segments.

### Content-Based Algorithms

*Cosine Similarity*: Measures the cosine of the angle between hotel feature vectors to determine similarity. Hotels with similar amenities, locations, and characteristics will have smaller angles between their feature vectors, indicating higher similarity.

*TF-IDF Vectorization*: Applied to hotel descriptions and reviews to extract important textual features. It identifies words that are important for specific hotels while filtering out common words that don't provide discriminative information.

*Feature Engineering*: The system extracts and creates meaningful features from hotel data, such as amenity combinations, location categories, price tiers, and derived metrics like value-for-money scores.

### Clustering and Segmentation

*K-Means Clustering*: Groups users with similar preferences into clusters, enabling targeted recommendations for each segment. For example, business travelers, luxury seekers, and budget-conscious families might form distinct clusters with different recommendation strategies.

*Hierarchical Clustering*: Creates a tree-like structure of user or hotel clusters, allowing for recommendations at different levels of granularity.


## Technologies Used

- *Django 5.2.1*: Web framework for rapid development
- *scikit-surprise 1.1.4*: Collaborative filtering algorithms
- *pandas 2.2.3*: Data manipulation and analysis
- *scikit-learn 1.6.1*: Machine learning algorithms

## Getting Started
Run the application in local by folowing the steps:

1. Clone the repository from github
2. Navigate to the project directory
3. Run the application in below approaches

    3.1. Run application using docker
    ```
    docker-compose build
    ```
    ```
    docker-compose up -d
    ```
        
    3.2. Run the application in local without docker
    
    1. Install the required dependencies using pip
        ```
        pip install poetry
        ```
        ```
        poetry install
        ```
    2. Migrate the model changes to DB
        ```
        python manage.py makemigrations
        ```
        ```
        python manage.py migrate
        ```
    3. Run the application
        ```
        python manage.py runserver
        ```
        
4. Access the aapplication in your web browser at http://localhost:8000/