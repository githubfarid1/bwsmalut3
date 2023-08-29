from django.urls import path
from .views import searchdoc, index

prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='searchdoc', view=searchdoc, name=prefix + 'searchdoc'),
    path(route='', view=index, name=prefix + 'index'),
    

]