from django import forms
from .models import Department

# creating a form  


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    filepath = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/pdf'}))
    uuid_id = forms.UUIDField(widget=forms.HiddenInput())

class DeletePdfFile(forms.Form):
    listdepartment = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(),
        to_field_name="name",
        required=True
    )
    box_number = forms.IntegerField() 
    doc_number = forms.IntegerField()
