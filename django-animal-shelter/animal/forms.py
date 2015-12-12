from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Animal

class SearchAndFilterForm(forms.ModelForm): ### TODO: dump all these definitions to the model, & use ModelForm here
    class Meta:
        model = Animal
        fields = ('breed', 'age', 'sex', 'size', 'is_neutered')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # override
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_action = '.'
        self.helper.disable_csrf = True
        self.helper.add_input(Submit('apply', 'Apply'))
