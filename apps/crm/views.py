import json

from django.shortcuts import render, get_object_or_404, redirect
from .models import Tag, Project
from .forms import (TagForm, ProjectForm)


def crm_home(request):
    return render(request, "crm/crm_home.html")


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, "crm/tag_list.html", {"tags": tags})


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
    return render(request, "crm/tag_form.html", {"form": form})


def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        tag.delete()
        return redirect("tag_list")
    return render(request, "crm/tag_confirm_delete.html", {"tag": tag})


def project_list(request):
    projects = Project.objects.all()
    return render(request, "crm/project_list.html", {"projects": projects})


def project_form_handler(request, project=None):
    if request.method == "POST":
        post_data = request.POST.copy()

        tag_ids_raw = post_data.get("tags", "[]").strip()

        # ✅ Преобразуем строку "1,5" в список [1, 5]
        try:
            if tag_ids_raw.startswith("["):
                tag_ids = json.loads(tag_ids_raw)  # Если это JSON-список
            else:
                tag_ids = [int(tag_id) for tag_id in tag_ids_raw.split(",") if tag_id.isdigit()]
        except (json.JSONDecodeError, ValueError):
            tag_ids = []

        # ✅ Правильно передаём в POST
        post_data.setlist("tags", [str(tag) for tag in tag_ids])

        # ✅ Передаём исправленные `post_data` в форму
        form = ProjectForm(post_data, request.FILES, instance=project)

        if form.is_valid():
            project = form.save(commit=False)
            project.save()

            # ✅ Теперь Django получает список объектов `Tag`
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
