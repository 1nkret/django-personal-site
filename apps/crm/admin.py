from django.contrib import admin
from apps.crm.models import Project, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    list_editable = ("color",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    filter_horizontal = ("tags",)
