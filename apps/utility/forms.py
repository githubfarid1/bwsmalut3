from django import forms
# creating a form  

class SearchQRCodeForm(forms.Form): 
    qrcode = forms.CharField(label="QR Code", max_length = 255, help_text = "Search QR Code") 

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()