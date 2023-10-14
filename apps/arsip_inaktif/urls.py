from django.urls import path
from .views import irigasi, air_baku, pantai, sungai, keuangan, tahun, report, pdfdownload, statistics, pdfremove, pdfupload

#tes2, tes1
prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='tahun/<str:year>', view=tahun, name=prefix + "tahun"),
    path(route='report', view=report, name=prefix + "report"),
    path(route='irigasi', view=irigasi, name=prefix + "irigasi"),
    path(route='air_baku', view=air_baku, name=prefix + "air_baku"),
    path(route='pantai', view=pantai, name=prefix + "pantai"),
    path(route='sungai', view=sungai, name=prefix + "sungai"),
    path(route='keuangan', view=keuangan, name=prefix + "keuangan"),
    path(route='pdfdownload/<str:uuid_id>', view=pdfdownload, name=prefix + 'pdfdownload'),
    path(route='', view=statistics, name=prefix + "statistics"),
    path(route='pdfremove/<str:uuid_id>', view=pdfremove, name=prefix + 'pdfremove'),
    path(route='pdfupload/<str:uuid_id>', view=pdfupload, name=prefix + 'pdfupload'),
    

]   