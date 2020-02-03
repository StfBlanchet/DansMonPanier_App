"""
dansMonPanier app
File that manages user creation form.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    first_name = forms.CharField(label="Nom d'utilisateur", max_length=18, help_text='Requis. 18 caractères max.')
    username = forms.CharField(label='Email', max_length=254, help_text='Requis. Veuillez entrer un email valide.')
    email = forms.EmailField(label='Confirmation de votre email', max_length=254, help_text='Requis. Veuillez entrer un email valide.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name',)
