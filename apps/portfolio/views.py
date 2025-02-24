from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from apps.crm.models import Project


def project_list(request):
    projects = Project.objects.all()
    paginator = Paginator(projects, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "portfolio/project_list.html", {"page_obj": page_obj})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    page = request.GET.get("page", 1)

    rating_overall_choices = Project._meta.get_field("rating_overall").choices
    rating_difficulty_choices = Project._meta.get_field("rating_difficulty").choices
    rating_usefulness_choices = Project._meta.get_field("rating_usefulness").choices

    return render(
        request,
        "portfolio/project_detail.html",
        {
            "project": project,
            "page": page,
            "rating_overall_choices": rating_overall_choices,
            "rating_difficulty_choices": rating_difficulty_choices,
            "rating_usefulness_choices": rating_usefulness_choices,
        },
    )
