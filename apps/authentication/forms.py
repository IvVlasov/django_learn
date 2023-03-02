from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .models import User


class UserConfirmForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """ is_confirmed is always True """
        kwargs['initial']['is_confirmed'] = True
        super(UserConfirmForm, self).__init__(*args, **kwargs)

    is_confirmed = forms.BooleanField(required=False, widget=forms.HiddenInput())
    code = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'contact_input'}))

    class Meta:
        model = User
        fields = ['is_confirmed']


class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'contact_input'}),
            'password': forms.PasswordInput(attrs={'class': 'contact_input'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact_input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'contact_input'}))
