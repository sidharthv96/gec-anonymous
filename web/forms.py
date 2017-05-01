from django import forms

from web.models import Tip


class AnonForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['subject', 'text', 'directed_to']
