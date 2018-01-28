from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Form cars_fleet/contact.html
class ContactForm(forms.Form):
    subject = forms.CharField(required=False, max_length=200)
    contact_email = forms.EmailField(max_length=200, label="Your email")
    message = forms.CharField(widget=forms.Textarea)


# Form cars_fleet/signup.html
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text="Required valid email address."
    )

    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2', )
