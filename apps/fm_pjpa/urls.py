from django.urls import path
from .views import atab, irwa_1, subfolder, tagged
prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='atab/<int:year>', view=atab, name=prefix + "atab"),
    path(route='irwa_1/<int:year>', view=irwa_1, name=prefix + "irwa_1"),
    path(route='subfolder/<int:id>', view=subfolder, name=prefix + "subfolder"),
    path(route='tagged/<str:slug>', view=tagged, name=prefix + "tagged"),
]