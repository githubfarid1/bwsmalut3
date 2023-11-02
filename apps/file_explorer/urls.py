from django.urls import path
from .views import tes
prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='tes', view=tes, name=prefix + "tes"),
]