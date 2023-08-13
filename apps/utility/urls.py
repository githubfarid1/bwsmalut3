from django.urls import path
from .views import qrcodesearch, upload

urlpatterns = [
    path(route='qrcodesearch', view=qrcodesearch, name="qrcodesearch"),
    path(route='upload', view=upload, name="upload"),

]