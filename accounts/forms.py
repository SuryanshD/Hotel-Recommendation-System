from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserPreference

FORM_INPUT_CLASS = "border focus:border-green-500 focus:ring-green-500 border-gray-300 outline-none rounded-md p-2 w-full"


class UserCreationForm(UserCreationForm):
    """Custom user creation form with additional fields for first name, last name, and email.

    This form inherits from Django's built-in UserCreationForm and adds fields for email, first name, and last name.
    It also customizes the widget attributes for better styling and user experience.
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = FORM_INPUT_CLASS
            if field_name == "password1":
                field.widget.attrs["placeholder"] = "Enter password"
            elif field_name == "password2":
                field.widget.attrs["placeholder"] = "Confirm password"
            else:
                field.widget.attrs["placeholder"] = f"Enter {field.label}"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class AuthenticationForm(AuthenticationForm):
    """
    Custom authentication form that inherits from Django's built-in AuthenticationForm.
    This form is used for user login and customizes the widget attributes for better styling.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = FORM_INPUT_CLASS
            if field_name == "username":
                field.widget.attrs["placeholder"] = "Enter username"
            elif field_name == "password":
                field.widget.attrs["placeholder"] = "Enter password"


class UserPreferenceForm(forms.ModelForm):
    """Form for user preferences, allowing selection of locations and amenities.
    This form is used to manage user preferences related to locations and amenities.
    It includes fields for selecting multiple locations and entering amenities as tags.
    """

    locations = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "select2-multiple",
                "data-placeholder": "Select cities...",
                "multiple": "multiple",
            }
        ),
    )
    amenities = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "tags-input border focus:border-green-500 focus:ring-green-500 border-gray-300 outline-none rounded-md p-2 w-full",
                "placeholder": "Enter amenities (press Enter to add)",
            }
        ),
    )

    class Meta:
        model = UserPreference
        fields = ["locations", "amenities", "price_range_from", "price_range_to"]
        widgets = {
            "price_range_from": forms.HiddenInput(),
            "price_range_to": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.locations:
                self.fields["locations"].initial = ",".join(self.instance.locations)
            if self.instance.amenities:
                self.fields["amenities"].initial = ",".join(self.instance.amenities)
