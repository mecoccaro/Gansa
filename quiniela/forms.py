from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True, help_text='Enter Email Address',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), )
    first_name = forms.CharField(max_length=100, required=True, help_text='Enter First Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), )
    last_name = forms.CharField(max_length=100, required=True, help_text='Enter Last Name',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), )
    username = forms.CharField(max_length=200, required=True, help_text='Enter Username',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), )
    password1 = forms.CharField(help_text='Enter Password', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}), )
    password2 = forms.CharField(required=True, help_text='Enter Password Again', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password Again'}), )
    check = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'check']


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico", max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No existe una cuenta con este correo electrónico.")
        return email
