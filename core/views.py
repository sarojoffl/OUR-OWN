from django.shortcuts import render, redirect
from .models import Project, Service, Feature, PricingPlan, ContactMessage, About, Story, TeamMember, FAQ
from django.contrib import messages
from .forms import ContactForm

def index(request):
    about = About.objects.first()
    services = Service.objects.all()
    features = Feature.objects.all()
    team_members = TeamMember.objects.all()
    faqs = FAQ.objects.all()
    pricing_plans = PricingPlan.objects.all()

    return render(request, 'core/index.html', {
        'about': about,
        'services': services,
        'features': features,
        'team_members': team_members,
        'faqs': faqs,
        'pricing_plans': pricing_plans,
    })

def about(request):
    about = About.objects.first()
    stories = Story.objects.all().order_by('-date')
    team = TeamMember.objects.all()
    return render(request, 'core/about.html', {
        'about': about,
        'stories': stories,
        'team': team
    })

def services(request):
    services = Service.objects.all()
    features = Feature.objects.all()
    pricing_plans = PricingPlan.objects.all()
    return render(request, 'core/service.html', {
        'services': services,
        'features': features,
        'pricing_plans': pricing_plans
    })

def projects(request):
    projects = Project.objects.all()
    return render(request, 'core/portfolio.html', {'projects': projects})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect('contact')
    else:
        form = ContactForm()

    faqs = FAQ.objects.all()
    return render(request, 'core/contact.html', {
        'form': form,
        'faqs': faqs
    })