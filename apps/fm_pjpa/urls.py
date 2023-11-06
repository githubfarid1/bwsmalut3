from django.urls import path
from .views import atab, irwa_1, subfolder, tagged, add_department, department, department_year
prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='atab/<int:year>', view=atab, name=prefix + "atab"),
    path(route='irwa_1/<int:year>', view=irwa_1, name=prefix + "irwa_1"),
    path(route='subfolder/<int:id>', view=subfolder, name=prefix + "subfolder"),
    path(route='tagged/<str:slug>', view=tagged, name=prefix + "tagged"),
    path(route='add_department', view=add_department, name=prefix + "add_department"),
    path(route='department/<str:slug>', view=department, name=prefix + "department"),
    path(route='department_year/<str:slug>/<int:year>', view=department_year, name=prefix + "department_year"),

]