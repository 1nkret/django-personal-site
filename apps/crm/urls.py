from django.urls import path
from .views import (tag_list, tag_create, tag_update,
                    tag_delete, project_list, project_create,
                    project_update, project_delete, crm_home)

urlpatterns = [
    path("", crm_home, name="crm_home"),

    path("tags/", tag_list, name="tag_list"),
    path("tags/create/", tag_create, name="tag_create"),
    path("tags/<int:pk>/edit/", tag_update, name="tag_update"),
    path("tags/<int:pk>/delete/", tag_delete, name="tag_delete"),

    path("projects/", project_list, name="crm_project_list"),
    path("projects/create/", project_create, name="crm_project_create"),
    path("projects/<int:pk>/edit/", project_update, name="crm_project_update"),
    path("projects/<int:pk>/delete/", project_delete, name="crm_project_delete"),
]
