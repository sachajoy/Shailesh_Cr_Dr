from django import forms
from django.forms.models import ModelForm

from . import models


class ClientForm(ModelForm):
    class Meta:
        model = models.Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in self.fields.items():
            self.fields[key].widget.attrs.update(
                {'class': 'form-control form-control-user'}
            )

class DateInput(forms.DateInput):
    input_type = 'date'


class TrancationForm(ModelForm):
    class Meta:
        model = models.Trancation
        fields = '__all__'
        widgets = {
            'date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in self.fields.items():
            self.fields[key].widget.attrs.update(
                {'class': 'form-control form-control-user'}
            )
