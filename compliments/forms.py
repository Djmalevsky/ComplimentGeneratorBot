# forms.py
from django import forms

class UploadFileForm(forms.Form):
    csv_file = forms.FileField()
    output_file_name = forms.CharField(max_length=100)
    compliment_prompt = forms.CharField(widget=forms.Textarea, required=False)  # Add a new field for the prompt