from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserCreationForm, AuthenticationForm, UserPreferenceForm
from .models import UserPreference
from hotel_booking_recommendation import settings


class AuthenticateView(LoginView):
    """Custom login view that handles user authentication.

    Once the user is authenticated, it checks if the user has set their preferences.
    If preferences are set, it redirects to the home page; otherwise, it redirects to the user preferences page.
    """

    form_class = AuthenticationForm
    template_name = "accounts/login.html"

    def get_success_url(self):
        user = self.request.user
        try:
            UserPreference.objects.get(user=user)
            return reverse_lazy(settings.LOGIN_REDIRECT_URL)
        except UserPreference.DoesNotExist:
            return reverse_lazy("user_preferences")


class RegisterView(CreateView):
    """Custom registration view for user sign-up"""

    form_class = UserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy(settings.LOGIN_URL)


class UserPreferencesView(View):
    """View to handle user preferences.
    This view allows users to set their preferences, including locations, amenities, and price range.
    """

    template_name = "accounts/preferences.html"
    model_name = UserPreference

    def get(self, request):
        user_preference, created = self.model_name.objects.get_or_create(
            user=request.user
        )
        form = UserPreferenceForm(instance=user_preference)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        user_preference, created = self.model_name.objects.get_or_create(
            user=request.user
        )
        user_preference.user = request.user

        locations_list = request.POST.getlist('locations')
        if locations_list:
            user_preference.locations = [loc.strip() for loc in locations_list if loc.strip()]
        else:
            user_preference.locations = []

        amenities_list = request.POST.getlist('amenities')
        if amenities_list:
            user_preference.amenities = [amenity.strip() for amenity in amenities_list if amenity.strip()]
        else:
            user_preference.amenities = []

        price_from = request.POST.get("price_range_from")
        price_to = request.POST.get("price_range_to") 

        if price_from:
            user_preference.price_range_from = float(price_from)
        if price_to:
            user_preference.price_range_to = float(price_to)

        user_preference.save()
        return redirect("/booking")
