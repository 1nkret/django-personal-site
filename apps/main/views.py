from django.shortcuts import render
from apps.crm.models import MainPageSettings, Project


def home(request):
    settings = MainPageSettings.objects.first()
    projects = Project.objects.all()[:6]
    return render(request, 'home.html', {'settings': settings, 'projects': projects})
