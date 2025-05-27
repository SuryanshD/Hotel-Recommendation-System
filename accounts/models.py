from django.db import models
from django.contrib.auth.models import User

from accounts.utility.field import ListField


class UserPreference(models.Model):
    """Model representing user preferences.

    This model stores preferences for a user, including locations, amenities,
    and price range. It is linked to the User model via a one-to-one relationship.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userpreference")
    locations = ListField(null=True, blank=True)
    amenities = ListField(null=True, blank=True)
    price_range_from = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    price_range_to = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s preferences"
