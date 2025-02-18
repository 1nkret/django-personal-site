from django.shortcuts import render
from apps.crm.models import Project


def project_list(request):
    projects = Project.objects.all()
    return render(request, "portfolio/project_list.html", {"projects": projects})
