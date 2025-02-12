from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm


def project_list(request):
    projects = Project.objects.all()
    return render(request, "portfolio/project_list.html", {"projects": projects})


def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("project_list")
    else:
        form = ProjectForm()
    return render(request, "portfolio/project_form.html", {"form": form})


def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project_list")
    else:
        form = ProjectForm(instance=project)
    return render(request, "portfolio/project_form.html", {"form": form})


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect("project_list")
    return render(request, "portfolio/project_confirm_delete.html", {"project": project})

