from django import forms

from .models import Shorturl

class UrlForm(forms.ModelForm):
    orig_url = forms.URLField(
        label='',
        widget=forms.TextInput(attrs={"placeholder": "http://www.tesla.com"})
    )
    word_url_bool = forms.BooleanField(
        required=False,
        label='Three Word URL:'
    )

    class Meta:
        model = Shorturl
        fields = [
            'orig_url',
            'word_url_bool'
        ]