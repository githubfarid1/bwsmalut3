from django.urls import path
from .views import searchdoc, index, sertifikat, bpkb_mobil_dan_motor, pdfupload

prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='searchdoc', view=searchdoc, name=prefix + 'searchdoc'),
    path(route='', view=index, name=prefix + 'index'),
    path(route='sertifikat', view=sertifikat, name=prefix + 'sertifikat'),
    path(route='bpkb_mobil_dan_motor', view=bpkb_mobil_dan_motor, name=prefix + 'bpkb_mobil_dan_motor'),
    path(route='pdfupload/<str:uuid_id>', view=pdfupload, name=prefix + 'pdfupload'),


]