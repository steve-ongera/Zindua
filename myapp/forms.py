# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ServiceProvider, LaundryPricing, ServiceVideo, Booking, Review
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.models import BaseUserManager

from .models import User

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username','email', 'phone_number', 'role', 'location', 'profile_picture', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Encrypt password
        if commit:
            user.save()
        return user




class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Email or Username")


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'role', 'location', 'profile_picture']

class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['category', 'bio', 'experience_years', 'id_number']

class LaundryPricingForm(forms.ModelForm):
    class Meta:
        model = LaundryPricing
        fields = ['basket_size', 'price', 'description']

class ServiceVideoForm(forms.ModelForm):
    class Meta:
        model = ServiceVideo
        fields = ['title', 'video_file', 'description']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service_date', 'location', 'special_instructions']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


