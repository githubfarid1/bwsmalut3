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
