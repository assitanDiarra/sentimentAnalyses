from django import forms
from django.forms import ModelForm

from .models import Tweets,Promise


class DateInput(forms.DateInput):
    input_type = 'date'


class PromiseForm(ModelForm):

    class Meta:
        model = Promise
        fields = ['title', 'description', 'made_on']
        widgets = {
            'made_on': DateInput(),
        }