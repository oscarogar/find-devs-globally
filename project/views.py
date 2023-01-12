from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from django.contrib import messages
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProjects
# Create your views here.

def project(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6 )

    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'project/projects.html', context)

def projects(request, pk):
    projectObj= Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        # UPDATE REVIEW
        messages.success(request, 'Your review was successful')
        projectObj.getVoteCount
        return redirect('projects', pk = projectObj.id)

    context =  {'project':projectObj, 'form': form}
    return render(request, 'project/project2.html', context)

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST': 
        newtags = request.POST.get('newtags').capitalize().replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form': form}
    return render(request, 'project/project_form.html', context)
    
@login_required(login_url='login')
def updateProject(request, id):
    #get user profile to prevent unauthorised access
    profile = request.user.profile
    #query the project using id
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)
    if request.method == 'POST': 
        newtags = request.POST.get('newtags').capitalize().replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form': form, 'project': project}
    return render(request, 'project/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, id):
     #get user profile to prevent unauthorised access
    profile = request.user.profile
    #query the project using id
    project_id = profile.project_set.get(id=id)
    if request.method == 'POST':
        project_id.delete()
        return redirect('project')
    context = {'object': project_id}
    return render(request, 'delete_template.html', context)
