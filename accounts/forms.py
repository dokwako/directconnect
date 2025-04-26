from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'role',
            'first_name',
            'last_name',
            'phone_number',
            'default_pickup_address',
            'default_delivery_address',
            'employee_id',
            'assigned_vehicles',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'default_pickup_address',
            'default_delivery_address',
        ]
