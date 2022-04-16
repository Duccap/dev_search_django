from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import context
from .models import Project,Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
# Create your views here.



def projects(request):
    projects= Project.objects.all()
    context= {'projects':projects}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    return render(request,'projects/single-project.html',{'projectObj':projectObj,'tags':tags})

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES ) #request.FILES in charge of receiving files like images etc 
        if form.is_valid():
            form.save()
            return redirect('projects')
    context={'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url='login')
def updateProject(request,pk):
    project= Project.objects.get(id=pk)
    form = ProjectForm(instance=project) #this function let django now it will modify the "instance" project instead of creating a new one
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context={'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url='login')
def deleteProject(request,pk):
    project= Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context={'object':project}
    return render(request,'projects/delete_template.html',context)