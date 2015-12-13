from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Animal

class SearchAndFilterForm(forms.ModelForm): ### TODO: dump all these definitions to the model, & use ModelForm here
    class Meta:
        model = Animal
        fields = ('breed', 'age', 'sex', 'size', 'is_neutered')