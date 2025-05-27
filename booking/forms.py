from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Hotel, Room, Booking, Review, SearchHistory
from datetime import date, timedelta


class HotelSearchForm(forms.Form):
    """
    Form for searching hotels based on various criteria.

    This form includes fields for city, area, check-in and check-out dates,
    number of guests, and amenities.
    It also includes validation to ensure that the check-in date is not in the past,
    the check-out date is after the check-in date, and the number of guests is not more than the room capacity.
    """

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Enter city name"}
        ),
    )
    area = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Enter area (optional)"}
        ),
    )
    check_in_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-input",
                "type": "date",
                "min": date.today().strftime("%Y-%m-%d"),
            }
        )
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-input",
                "type": "date",
                "min": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
            }
        )
    )
    guests = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=2,
        widget=forms.NumberInput(
            attrs={"class": "form-input", "min": "1", "max": "10"}
        ),
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "form-input", "placeholder": "Min price per night"}
        ),
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "form-input", "placeholder": "Max price per night"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in_date")
        check_out = cleaned_data.get("check_out_date")
        min_price = cleaned_data.get("min_price")
        max_price = cleaned_data.get("max_price")

        if check_in and check_out:
            if check_in >= check_out:
                raise ValidationError("Check-out date must be after check-in date.")

            if check_in < date.today():
                raise ValidationError("Check-in date cannot be in the past.")

        if min_price and max_price and min_price > max_price:
            raise ValidationError("Minimum price cannot be greater than maximum price.")

        return cleaned_data


class BookingForm(forms.ModelForm):
    """
    Form for booking a room.

    This form includes fields for check-in and check-out dates, number of guests, and special requests.
    It also includes validation to ensure that the check-in date is not in the past,
    the check-out date is after the check-in date, and the number of guests is not more than the room capacity.
    """

    class Meta:
        model = Booking
        fields = ["check_in_date", "check_out_date", "guests", "special_requests"]
        widgets = {
            "check_in_date": forms.DateInput(
                attrs={
                    "class": "form-input",
                    "type": "date",
                    "min": date.today().strftime("%Y-%m-%d"),
                }
            ),
            "check_out_date": forms.DateInput(
                attrs={
                    "class": "form-input",
                    "type": "date",
                    "min": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            ),
            "guests": forms.NumberInput(
                attrs={"class": "form-input", "min": "1", "max": "10"}
            ),
            "special_requests": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 3,
                    "placeholder": "Any special requests or requirements...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop("room", None)
        super().__init__(*args, **kwargs)

        if self.room:
            self.fields["guests"].widget.attrs["max"] = str(self.room.capacity)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in_date")
        check_out = cleaned_data.get("check_out_date")
        guests = cleaned_data.get("guests")

        if check_in and check_out:
            if check_in >= check_out:
                raise ValidationError("Check-out date must be after check-in date.")

            if check_in < date.today():
                raise ValidationError("Check-in date cannot be in the past.")

        if self.room and guests and guests > self.room.capacity:
            raise ValidationError(
                f"This room can accommodate maximum {self.room.capacity} guests."
            )

        return cleaned_data


class ReviewForm(forms.ModelForm):
    """
    Form for creating or updating a review."""

    class Meta:
        model = Review
        fields = [
            "rating",
            "title", 
            "comment",
            "cleanliness_rating",
            "service_rating",
            "location_rating",
            "value_rating",
        ]
        widgets = {
            "rating": forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={"class": "form-select"},
            ),
            "title": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Review title"}
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 4,
                    "placeholder": "Share your experience...",
                }
            ),
            "cleanliness_rating": forms.Select(
                choices=[(i, f"{i}") for i in range(1, 6)],
                attrs={"class": "form-select"},
            ),
            "service_rating": forms.Select(
                choices=[(i, f"{i}") for i in range(1, 6)],
                attrs={"class": "form-select"},
            ),
            "location_rating": forms.Select(
                choices=[(i, f"{i}") for i in range(1, 6)],
                attrs={"class": "form-select"},
            ),
            "value_rating": forms.Select(
                choices=[(i, f"{i}") for i in range(1, 6)],
                attrs={"class": "form-select"},
            ),
        }


class HotelFilterForm(forms.Form):
    """
    Form for filtering hotels based on various criteria.
    """

    SORT_CHOICES = [
        ("rating", "Rating (High to Low)"),
        ("price_low", "Price (Low to High)"),
        ("price_high", "Price (High to Low)"),
        ("name", "Name (A to Z)"),
    ]

    HOTEL_TYPE_CHOICES = [
        ("", "All Types"),
        ("budget", "Budget"),
        ("mid_range", "Mid Range"),
        ("luxury", "Luxury"),
        ("resort", "Resort"),
        ("boutique", "Boutique"),
    ]

    STAR_RATING_CHOICES = [
        ("", "All Ratings"),
        ("5", "5 Stars"),
        ("4", "4+ Stars"),
        ("3", "3+ Stars"),
        ("2", "2+ Stars"),
        ("1", "1+ Stars"),
    ]

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial="rating",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    hotel_type = forms.ChoiceField(
        choices=HOTEL_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    star_rating = forms.ChoiceField(
        choices=STAR_RATING_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    amenities = forms.MultipleChoiceField(
        choices=[
            ("wifi", "WiFi"),
            ("pool", "Swimming Pool"),
            ("gym", "Gym"),
            ("spa", "Spa"),
            ("restaurant", "Restaurant"),
            ("bar", "Bar"),
            ("parking", "Parking"),
            ("ac", "Air Conditioning"),
            ("room_service", "Room Service"),
            ("laundry", "Laundry"),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-checkbox"}),
    )
