from django import forms
from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'filename',
            'description',
            'tags',
        ]
        widgets = {
            'tags': forms.TextInput(attrs={'data-role': 'tagsinput'}),
            'description': forms.Textarea(attrs={'rows': '3'}),
        }