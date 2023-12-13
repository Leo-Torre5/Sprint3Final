# user_management/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=250, required=False)
    last_name = forms.CharField(max_length=250, required=False)
    address = forms.CharField(max_length=400, required=False)
    city = forms.CharField(max_length=200, required=False)
    state = forms.CharField(max_length=100, required=False)
    zip_code = forms.CharField(max_length=10)

    class Meta:
        model = User  # Use the default User model
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'address', 'city', 'state', 'zip_code']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # Check if a UserProfile already exists for the user
        try:
            profile = user.userprofile
            # If the profile exists, update its fields
            profile.address = self.cleaned_data['address']
            profile.city = self.cleaned_data['city']
            profile.state = self.cleaned_data['state']
            profile.zip_code = self.cleaned_data['zip_code']
            profile.save()
        except UserProfile.DoesNotExist:
            # If the profile doesn't exist, create a new one
            UserProfile.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                zip_=self.cleaned_data['zip_code']
            )

        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'city', 'state', 'zip_code', 'image', ]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

    def as_crispy_field(self, *args, **kwargs):
        # Override the as_crispy_field method to remove the "Currently:" part
        return super().as_crispy_field(*args, **kwargs).replace("Currently:", "")

