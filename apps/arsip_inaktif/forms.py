from django import forms
from .models import Doc, Bundle
from django.forms import ModelForm

class SearchDoc(forms.Form):
    # def getcodes():
    #     codes = Bundle.objects.order_by("code").values("code").distinct()
    #     codelist = [(x['code'],x['code']) for x in codes if x['code'] !='']
    #     return codelist
    # code = forms.CharField(label='Kode Klasifikasi', widget=forms.Select(choices=getcodes()))
    search = forms.CharField(label="Kata Kunci")
