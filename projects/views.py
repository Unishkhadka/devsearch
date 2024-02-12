from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, pagination_projects
from django.db import IntegrityError

def projects(request):
    projects, search_query = search_projects(request)
    projects, custom_range = pagination_projects(request, projects, 3)
    context = {
        "projects": projects,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "projects/projects.html", context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == "POST":
        try:
            form = ReviewForm(request.POST)
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            project.getVoteCount
            messages.success(request, "Review added successfully")
        except IntegrityError:
            messages.error(request, "Review already added!")


        return redirect("project", pk=project.id)
    project = Project.objects.get(id=pk)
    context = {"project": project, "form": form}
    return render(request, "projects/single_project.html", context)


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid:
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("account")
    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid:
            form.save()
            return redirect("account")
    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    context = {"object": project}
    return render(request, "delete_template.html", context)
