from django import forms


class ContactUs(forms.Form):
    from_email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    honeypot = forms.CharField(max_length=255, required=False)
