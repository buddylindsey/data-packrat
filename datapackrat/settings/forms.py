from django import forms

from .models import Attribute


class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = [
            'template', 'template_attribute', 'order', 'start_joiner',
            'end_joiner'
        ]

    def clean_start_joiner(self):
        if (self.data['start_joiner'].startswith(' ')
                or self.data['start_joiner'].endswith(' ')):
            return self.data['start_joiner']

        return self.cleaned_data['start_joiner']

    def clean_end_joiner(self):
        if (self.data['end_joiner'].startswith(' ')
                or self.data['end_joiner'].endswith(' ')):
            return self.data['end_joiner']

        return self.cleaned_data['end_joiner']