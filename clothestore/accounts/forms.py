from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    """
    Form to sign in
    """
    first_name = forms.CharField(max_length=150, required=True, 
                widget= forms.TextInput(attrs={
                    "placeholder": 'First Name'
                }))
    last_name = forms.CharField(max_length=150, required=True, 
                widget= forms.TextInput(attrs={
                    "placeholder": 'Last Name'
                }))
    username = forms.CharField(max_length=150, required=True, 
                widget= forms.TextInput(attrs={
                    "placeholder": 'Username'
                }))
    email = forms.EmailField(max_length=150, required=True, 
                widget= forms.TextInput(attrs={
                    "placeholder": 'Email'
                }))
    
    

    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']