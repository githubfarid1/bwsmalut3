from django.urls import path
from .views import tahun, report
#tes2, tes1
prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='tahun/<str:year>', view=tahun, name=prefix + "tahun"),
    path(route='report', view=report, name=prefix + "report"),

]   