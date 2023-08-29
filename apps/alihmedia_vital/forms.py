from django import forms
from .models import Variety
class SearchDoc(forms.Form):
    folder = forms.ModelChoiceField(
        queryset=Variety.objects.all(),
        widget=forms.Select(),
        to_field_name="folder",
        required=True, label="Jenis Dokumen"
    )
    search = forms.CharField(required=False)

class InserPdfDoc(forms.Form):
    folder = forms.ModelChoiceField(
        queryset=Variety.objects.all(),
        widget=forms.Select(),
        to_field_name="folder",
        required=True, label="Jenis Dokumen"
    )

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    filepath = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/pdf'}))
    uuid_id = forms.UUIDField(widget=forms.HiddenInput())
