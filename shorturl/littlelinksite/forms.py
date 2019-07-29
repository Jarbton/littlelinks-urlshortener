from django import forms

from .models import Shorturl

class UrlForm(forms.ModelForm):
    orig_url = forms.URLField(
        label='',
        widget=forms.TextInput(attrs={"placeholder": "http://www.tesla.com"})
    )

    class Meta:
        model = Shorturl
        fields = [
            'orig_url'
        ]