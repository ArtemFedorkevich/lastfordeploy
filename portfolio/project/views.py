from django.shortcuts import render
from .models import Project
from blog.models import Post
import os

def project_index(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'project_index.html', context)


def project_detail(request, pk):
    if pk==1:
        project = Project.objects.get(pk=pk)
        context = {
            'project': project
        }

        return render(request, 'project_detailbutton.html', context)
    elif pk==2:
        project = Project.objects.get(pk=pk)
        context = {
            'project': project
        }
        posts = Post.objects.all().order_by('-created_on')
        contextblog = {
            "posts": posts,
        }
        return render(request, 'project_detailswithblogbutton.html', context)
    elif pk==3:
        project = Project.objects.get(pk=pk)
        context = {
            'project': project
        }
        posts = Post.objects.all().order_by('-created_on')
        contextblog = {
            "posts": posts,
        }
        return render(request, 'project_detailresume.html', context)
    else:
        project = Project.objects.get(pk=pk)
        context = {
            'project': project
        }



        return render(request, 'project_detail.html', context)

