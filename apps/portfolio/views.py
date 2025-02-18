from django.core.paginator import Paginator
from django.shortcuts import render
from apps.crm.models import Project


def project_list(request):
    projects = Project.objects.all()
    paginator = Paginator(projects, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "portfolio/project_list.html", {"page_obj": page_obj})
