from django.shortcuts import render
from apps.crm.models import MainPageSettings, MainPageProjects, Project


def home(request):
    settings = MainPageSettings.objects.first()
    main_page_projects = MainPageProjects.objects.first()

    projects = (
        main_page_projects.projects.order_by("mainpageprojectorder__order")
        if main_page_projects else []
    )

    return render(
        request=request,
        template_name="home.html",
        context={
            "settings": settings,
            "projects": projects,
            "all_projects": Project.objects.all()
        }
    )
