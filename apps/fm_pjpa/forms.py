from django import forms
from .models import File, Department, Subfolder

class FileForm(forms.ModelForm):
    fileupload = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept':'application/vnd.ms-excel, image/*, application/pdf, application/msword, application/vnd.ms-powerpoint'}))
    class Meta:
        model = File
        fields = [
            # 'filename',
            'description',
            'tags',
        ]
        widgets = {
            'tags': forms.TextInput(attrs={'data-role': 'tagsinput'}),
            'description': forms.Textarea(attrs={'rows': '3'}),
            # 'filename': forms.FileInput(attrs={'accept':'application/vnd.ms-excel, image/*, application/pdf, application/msword, application/vnd.ms-powerpoint'})
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'name',
            'shortname',
        ]


class SubfolderForm(forms.ModelForm):
    class Meta:
        model = Subfolder
        fields = [
            'name',
        ]
