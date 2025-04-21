from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'input'}))
    password1 = forms.CharField(max_length=50, required=True,
                                widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(max_length=50, required=True,
                                widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ['username', 'password']
