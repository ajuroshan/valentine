from django import forms
from .models import Applications

class ApplicationsForm(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ['age', 'gender', 'interests', 'campus', 'year', 'match_with_same_year', 'match_with_same_campus']
        widgets = {
            'interests': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ApplicationsForm, self).__init__(*args, **kwargs)
        # You can customize form attributes here, e.g., add placeholders or help_text
        self.fields['gender'].empty_label = "Select Gender"
        self.fields['year'].empty_label = "Select Year"
        self.fields['campus'].empty_label = "Select Campus"
