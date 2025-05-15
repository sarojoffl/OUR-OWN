from django.shortcuts import render, redirect
from .models import Project, Service, Feature, PricingPlan, About, Story, TeamMember, FAQ, Testimonial, BlogPost
from django.contrib import messages
from django.shortcuts import get_object_or_404


def index(request):
    about = About.objects.first()
    services = Service.objects.all().order_by('-id')[:3]
    features = Feature.objects.all()
    team_members = TeamMember.objects.all()
    faqs = FAQ.objects.all()
    pricing_plans = PricingPlan.objects.all()
    testimonials = Testimonial.objects.all()
    blogs = BlogPost.objects.all().order_by('-publish_date')[:3]

    return render(request, 'core/index.html', {
        'about': about,
        'services': services,
        'features': features,
        'team_members': team_members,
        'faqs': faqs,
        'pricing_plans': pricing_plans,
        'testimonials': testimonials,
        'blogs': blogs
    })

def about(request):
    about = About.objects.first()
    stories = list(Story.objects.all().order_by('-date'))
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

def services_detail(request, slug):
    services = get_object_or_404(Service, slug=slug)
    return render(request, 'core/service_detail.html', {
        'services': services
    })

def projects(request):
    projects = Project.objects.all()
    return render(request, 'core/portfolio.html', {'projects': projects})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm, TestimonialForm
from .models import FAQ

def contact(request):
    if request.method == "POST":
        if 'name' in request.POST and 'email' in request.POST:
            # Handle Contact Form submission
            form = ContactForm(request.POST)
            testimonial_form = TestimonialForm()  # empty for now
            if form.is_valid():
                form.save()
                messages.success(request, "Your message has been sent successfully.")
                return redirect('contact')
        elif 'customer_name' in request.POST and 'profession' in request.POST:
            # Handle Testimonial Form submission
            testimonial_form = TestimonialForm(request.POST, request.FILES)
            form = ContactForm()  # empty for now
            if testimonial_form.is_valid():
                testimonial_form.save()
                messages.success(request, "Your testimonial has been submitted successfully.")
                return redirect('contact')
        else:
            # Unexpected POST data
            form = ContactForm()
            testimonial_form = TestimonialForm()
    else:
        form = ContactForm()
        testimonial_form = TestimonialForm()

    faqs = FAQ.objects.all()
    return render(request, 'core/contact.html', {
        'form': form,
        'testimonial_form': testimonial_form,
        'faqs': faqs
    })


def blog(request):
    blogs = BlogPost.objects.all().order_by('-publish_date')
    return render(request, 'core/blog.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'core/blog_detail.html', {'blog': blog})

def book_plan(request, plan_id):
    plan = get_object_or_404(PricingPlan, id=plan_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            customer = form.save(commit=False)
            customer.plan = plan
            customer.save()
            return render(request, 'core/booking_confirmation.html', {'customer': customer})
    else:
        form = BookingForm(initial={'plan': plan})
    return render(request, 'core/book_now.html', {'form': form, 'plan': plan})
