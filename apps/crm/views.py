import json

from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models

from .models import Tag, Project, MainPageSettings, MainPageProjects, MainPageProjectOrder
from .forms import (TagForm, ProjectForm, MainPageSettingsForm, MainPageProjectsForm)


def tag_list(request):
    tags = Tag.objects.all()
    paginator = Paginator(tags, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "crm/tag_list.html", {"tags": tags, "page_obj": page_obj})


def tag_create(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tag_list")
    else:
        form = TagForm()
    return render(request, "crm/tag_form.html", {"form": form})


def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect("tag_list")
    else:
        form = TagForm(instance=tag)
    return render(request, "crm/tag_form.html", {"form": form, "tag": tag})


def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        tag.delete()
        return redirect("tag_list")
    return render(request, "crm/tag_confirm_delete.html", {"tag": tag})


def project_list(request):
    projects = Project.objects.all()
    paginator = Paginator(projects, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "crm/project_list.html", {"projects": projects, "page_obj": page_obj})


def project_form_handler(request, project=None):
    if request.method == "POST":
        post_data = request.POST.copy()

        # ✅ Обрабатываем удаление изображения
        if post_data.get("remove_image") == "true" and project and project.image:
            default_storage.delete(project.image.path)
            project.image = None
            project.save()

        tag_ids_raw = post_data.get("tags", "[]").strip()
        try:
            if tag_ids_raw.startswith("["):
                tag_ids = json.loads(tag_ids_raw)
            else:
                tag_ids = [int(tag_id) for tag_id in tag_ids_raw.split(",") if tag_id.isdigit()]
        except (json.JSONDecodeError, ValueError):
            tag_ids = []

        post_data.setlist("tags", [str(tag) for tag in tag_ids])

        form = ProjectForm(post_data, request.FILES, instance=project)

        if form.is_valid():
            project = form.save(commit=False)

            # Убеждаемся, что end_date не раньше start_date
            if project.end_date and project.end_date < project.start_date:
                form.add_error("end_date", "Дата завершения не может быть раньше даты начала.")
            else:
                project.save()
                project.tags.set(Tag.objects.filter(id__in=tag_ids))
                return redirect("crm_project_list")

    else:
        form = ProjectForm(instance=project)

    tag_ids_json = json.dumps(list(form.instance.tags.values_list("id", flat=True))) if form.instance.pk else "[]"

    return render(request, "crm/project_form.html", {
        "form": form,
        "project": project,
        "tag_ids_json": tag_ids_json
    })


def project_create(request):
    return project_form_handler(request)


def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return project_form_handler(request, project)


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect("crm_project_list")
    return render(request, "crm/project_confirm_delete.html", {"project": project})


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Max
import json
from .models import MainPageSettings, MainPageProjects, MainPageProjectOrder, Project
from .forms import MainPageSettingsForm

def main_page_settings(request):
    settings, created = MainPageSettings.objects.get_or_create(id=1)
    main_page_projects, created = MainPageProjects.objects.get_or_create(id=1)
    ordered_projects = MainPageProjectOrder.objects.filter(main_page=main_page_projects).order_by("order")

    if request.method == "POST":
        if "save_settings" in request.POST:
            form = MainPageSettingsForm(request.POST, instance=settings)
            if form.is_valid():
                form.save()

        if "remove_project" in request.POST:
            project_id = request.POST.get("remove_project")
            MainPageProjectOrder.objects.filter(project_id=project_id, main_page=main_page_projects).delete()

        return redirect("main_page_settings")

    form = MainPageSettingsForm(instance=settings)
    all_projects = Project.objects.all()

    return render(request, "crm/main_page_settings.html", {"form": form, "projects": ordered_projects, "all_projects": all_projects})


def move_project_ajax(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        direction = request.POST.get("direction")

        main_page_projects, _ = MainPageProjects.objects.get_or_create(id=1)
        project_order = get_object_or_404(MainPageProjectOrder, main_page=main_page_projects, project_id=project_id)

        if direction == "up":
            prev_project = (
                MainPageProjectOrder.objects.filter(main_page=main_page_projects, order__lt=project_order.order)
                .order_by("-order")
                .first()
            )
            if prev_project:
                prev_project.order, project_order.order = project_order.order, prev_project.order
                prev_project.save()
                project_order.save()

        elif direction == "down":
            next_project = (
                MainPageProjectOrder.objects.filter(main_page=main_page_projects, order__gt=project_order.order)
                .order_by("order")
                .first()
            )
            if next_project:
                next_project.order, project_order.order = project_order.order, next_project.order
                next_project.save()
                project_order.save()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)


def add_project_to_main(request):
    if request.method == "POST":
        data = json.loads(request.body)
        project_id = data.get("project_id")

        main_page_projects, created = MainPageProjects.objects.get_or_create(id=1)

        if not MainPageProjectOrder.objects.filter(project_id=project_id, main_page=main_page_projects).exists():
            max_order = (
                MainPageProjectOrder.objects.filter(main_page=main_page_projects).aggregate(Max("order"))["order__max"]
                or 0
            )
            MainPageProjectOrder.objects.create(main_page=main_page_projects, project_id=project_id, order=max_order + 1)

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)


def remove_project_ajax(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")

        main_page_projects, _ = MainPageProjects.objects.get_or_create(id=1)
        deleted_count, _ = MainPageProjectOrder.objects.filter(project_id=project_id, main_page=main_page_projects).delete()

        if deleted_count > 0:
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "not_found"}, status=404)

    return JsonResponse({"status": "error"}, status=400)


