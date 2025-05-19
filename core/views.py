from django.shortcuts import render, redirect
from .models import Project, Service, Feature, About, FAQ, Testimonial, BlogPost, Booking, CarouselItem
from .forms import BookingForm, ContactForm, TestimonialForm
from django.contrib import messages
from django.shortcuts import get_object_or_404

def index(request):
    about = About.objects.first()
    services = Service.objects.all().order_by('-id')[:3]
    features = Feature.objects.all()
    faqs = FAQ.objects.all()
    testimonials = Testimonial.objects.all()
    blogs = BlogPost.objects.all().order_by('-publish_date')[:3]
    carousel_items = CarouselItem.objects.all()

    return render(request, 'core/index.html', {
        'about': about,
        'services': services,
        'features': features,
        'faqs': faqs,
        'testimonials': testimonials,
        'blogs': blogs,
        'carousel_items': carousel_items,
    })

def about(request):
    about = About.objects.first()
    return render(request, 'core/about.html', {
        'about': about,
    })

def services(request):
    services = Service.objects.all()
    features = Feature.objects.all()
    return render(request, 'core/service.html', {
        'services': services,
        'features': features,
    })

def services_detail(request, slug):
    services = get_object_or_404(Service, slug=slug)
    return render(request, 'core/service_detail.html', {
        'services': services
    })

def projects(request):
    projects = Project.objects.all()
    return render(request, 'core/portfolio.html', {'projects': projects})

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
    recent_blogs = BlogPost.objects.order_by('-publish_date')[:5]
    return render(request, 'core/blog_detail.html', {
        'blog': blog,
        'recent_blogs': recent_blogs,
    })

def book_service(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return render(request, 'core/booking_confirmation.html', {'booking': booking})
    else:
        form = BookingForm()

    # Fetch all services and FAQs to display on the booking page
    services = Service.objects.all()
    faqs = FAQ.objects.all()

    return render(request, 'core/book_now.html', {'form': form, 'services': services, 'faqs': faqs})