from django.shortcuts import render, redirect

def index(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def services(request):
    return render(request, 'core/service.html')

def projects(request):
    projects = Project.objects.all()
    return render(request, 'core/portfolio.html', {'projects': projects})

def contact(request):
    return render(request, 'core/contact.html')