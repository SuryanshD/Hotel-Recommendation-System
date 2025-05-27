from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.utility.field import ListField
from decimal import Decimal


class Hotel(models.Model):
    """Model representing a hotel with various attributes and methods for managing hotel data."""

    HOTEL_TYPES = [
        ("budget", "Budget"),
        ("mid_range", "Mid Range"),
        ("luxury", "Luxury"),
        ("resort", "Resort"),
        ("boutique", "Boutique"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    hotel_type = models.CharField(
        max_length=20, choices=HOTEL_TYPES, default="mid_range"
    )
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    amenities = ListField(blank=True, null=True)  # ['wifi', 'pool', 'gym', 'spa']
    star_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    images = ListField(blank=True, null=True)  # List of image URLs
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    check_in_time = models.TimeField(default="14:00")
    check_out_time = models.TimeField(default="11:00")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-average_rating", "name"]

    def __str__(self):
        return f"{self.name} - {self.city}"

    def update_rating(self):
        """Update average rating based on reviews"""
        reviews = self.reviews.all()
        if reviews:
            self.average_rating = (
                reviews.aggregate(avg_rating=models.Avg("rating"))["avg_rating"] or 0.0
            )
            self.total_reviews = reviews.count()
        else:
            self.average_rating = 0.0
            self.total_reviews = 0
        self.save()

    @property
    def min_price(self):
        """Get minimum room price for this hotel"""
        min_price = self.rooms.filter(is_available=True).aggregate(
            min_price=models.Min('price_per_night')
        )['min_price']
        return min_price or 0

    @property
    def max_price(self):
        """Get maximum room price for this hotel"""
        max_price = self.rooms.filter(is_available=True).aggregate(
            max_price=models.Max('price_per_night')
        )['max_price']
        return max_price or 0

    @property
    def price_range(self):
        """Get price range as a formatted string"""
        min_p = self.min_price
        max_p = self.max_price
        if min_p == max_p:
            return f"₹{min_p:,.0f}"
        return f"₹{min_p:,.0f} - ₹{max_p:,.0f}"
    
    @property
    def image(self):
        """Get the first image from the images list for backward compatibility"""
        if self.images and len(self.images) > 0:
            return self.images[0]
        return None
    
    @property
    def has_multiple_images(self):
        """Check if hotel has multiple images"""
        return self.images and len(self.images) > 1




class Room(models.Model):
    """Model representing a hotel room with various attributes and methods for managing room data."""

    ROOM_TYPES = [
        ("single", "Single"),
        ("double", "Double"),
        ("twin", "Twin"),
        ("suite", "Suite"),
        ("family", "Family"),
        ("deluxe", "Deluxe"),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    size_sqft = models.IntegerField(null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = ListField(blank=True, null=True)  # ['ac', 'tv', 'minibar', 'balcony']
    description = models.TextField(blank=True)
    images = ListField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["hotel", "room_number"]
        ordering = ["price_per_night"]

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type} {self.room_number}"
    
    @property
    def image(self):
        """Get the first image from the images list for backward compatibility"""
        if self.images and len(self.images) > 0:
            return self.images[0]
        return None
    
    @property
    def has_multiple_images(self):
        """Check if room has multiple images"""
        return self.images and len(self.images) > 1


class Booking(models.Model):
    """Model representing a hotel booking with various attributes and methods for managing bookings."""

    BOOKING_STATUS = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("checked_in", "Checked In"),
        ("checked_out", "Checked Out"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField(validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(
        max_length=20, choices=BOOKING_STATUS, default="pending"
    )
    special_requests = models.TextField(blank=True)
    booking_reference = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.user.username}"

    @property
    def nights(self):
        return (self.check_out_date - self.check_in_date).days

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import uuid

            self.booking_reference = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)


class Review(models.Model):
    """Model representing a hotel review with various attributes and methods for managing reviews."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="reviews")
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name="review", null=True, blank=True
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    cleanliness_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    service_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    location_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    value_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "hotel"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name} ({self.rating}/5)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update hotel rating after saving review
        self.hotel.update_rating()


class UserInteraction(models.Model):
    """Track user interactions for recommendation system"""

    INTERACTION_TYPES = [
        ("view", "View"),
        ("search", "Search"),
        ("book", "Book"),
        ("review", "Review"),
        ("wishlist", "Wishlist"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="interactions"
    )
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="interactions"
    )
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    weight = models.DecimalField(
        max_digits=3, decimal_places=2, default=1.0
    )  # Different weights for different interactions
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.hotel.name}"


class SearchHistory(models.Model):
    """Store user search history for recommendations"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="search_history"
    )
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField()
    min_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    amenities = ListField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.city} ({self.check_in_date})"
