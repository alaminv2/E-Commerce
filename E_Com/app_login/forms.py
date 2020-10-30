from django import forms
from app_login.models import User, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class signUpForm(UserCreationForm):
    # email = forms.EmailField(label="", widget=forms.TextInput(
    #     attrs={'placeholder': 'Something@gmail.com'}))
    # password1 = forms.PasswordInput(
    #     label="", widget=forms.TextInput(attrs={'placeholder': 'Password'}))
    # password2 = forms.PasswordInput(label="", widget=forms.TextInput(
    #     attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


# class loginForm(AuthenticationForm):
#     email = forms.EmailField(label="", widget=forms.TextInput(attrs={'placeholder' : 'Something@gmail.com'}))
#     password1 = forms.PasswordInput(label = "", widget=forms.TextInput(attrs={'placeholder' : 'Password'}))

#     class Meta:
#         model =


class profileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
