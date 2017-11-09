from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(required=False, max_length=200)
    contact_email = forms.EmailField(max_length=200, label="Your email")
    message = forms.CharField(widget=forms.Textarea)
