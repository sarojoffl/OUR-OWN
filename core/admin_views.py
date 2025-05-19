from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Booking, Service, BlogPost, ContactMessage, FAQ, Testimonial, About, Feature, OrganizationInfo, CarouselItem
from .forms import BlogPostForm, FAQForm, BookingStatusForm, AboutForm, ServiceForm, FeatureForm, TestimonialForm, OrganizationInfoForm, CarouselItemForm

# ---------- DASHBOARD ----------
@login_required
def admin_dashboard(request):
    context = {
        'total_bookings': Booking.objects.count(),
        'total_services': Service.objects.count(),
        'total_blogs': BlogPost.objects.count(),
        'total_messages': ContactMessage.objects.count(),
        'total_faqs': FAQ.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
        'total_features': Feature.objects.count(),
        'recent_bookings': Booking.objects.order_by('-booked_on')[:5],
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
        'current_year': datetime.now().year,
    }
    return render(request, 'admin/dashboard.html', context)

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'admin/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('home')

# ---------- CONTACT MESSAGES ----------
@login_required
def admin_contact_messages(request):
    contact_messages = ContactMessage.objects.order_by('-created_at')
    return render(request, 'admin/contact_messages.html', {'contact_messages': contact_messages})

@login_required
def admin_delete_contact_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    if request.method == "POST":
        message.delete()
        messages.success(request, 'Message deleted successfully.')
        return redirect('admin_contact_messages')
    return render(request, 'admin/delete_contact_message.html', {'message': message})

# ---------- BLOG ----------
@login_required
def admin_add_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post added successfully.")
            return redirect('admin_view_blog_posts')
    else:
        form = BlogPostForm()
    return render(request, 'admin/blog_form.html', {'form': form, 'action': 'Add'})

@login_required
def admin_view_blog_posts(request):
    posts = BlogPost.objects.order_by('-publish_date')
    return render(request, 'admin/view_blog_posts.html', {'posts': posts})

@login_required
def admin_update_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully.")
            return redirect('admin_view_blog_posts')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'admin/blog_form.html', {'form': form, 'post': post, 'action': 'Update'})

@login_required
def admin_delete_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Blog post deleted successfully.")
        return redirect('admin_view_blog_posts')
    return render(request, 'admin/delete_blog_post.html', {'post': post})

# ---------- FAQ ----------
@login_required
def admin_view_faq(request):
    return render(request, 'admin/faq.html')

@login_required
def admin_view_faqs(request):
    faqs = FAQ.objects.all()
    return render(request, 'admin/faq_list.html', {'faqs': faqs})

@login_required
def admin_add_faq(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ added successfully.")
            return redirect('admin_view_faqs')
    else:
        form = FAQForm()
    return render(request, 'admin/faq_form.html', {'form': form, 'action': 'Add'})

@login_required
def admin_update_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ updated successfully.")
            return redirect('admin_view_faqs')
    else:
        form = FAQForm(instance=faq)
    return render(request, 'admin/faq_form.html', {'form': form, 'action': 'Update'})

@login_required
def admin_delete_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == 'POST':
        faq.delete()
        messages.success(request, "FAQ deleted successfully.")
        return redirect('admin_view_faqs')
    return render(request, 'admin/faq_confirm_delete.html', {'faq': faq})

# ---------- BOOKINGS ----------
@login_required
def admin_view_bookings(request):
    bookings = Booking.objects.all().order_by('-booked_on')
    return render(request, 'admin/view_bookings.html', {'bookings': bookings})

@login_required
def admin_update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        admin_comment = request.POST.get('admin_comment', '')
        if new_status and new_status != booking.status:
            booking.status = new_status
            booking.admin_comment = admin_comment
            booking.save()
            send_booking_status_email(booking)
            messages.success(request, f"Booking status updated to '{booking.get_status_display()}' successfully.")
        else:
            messages.info(request, "No changes were made to the booking status.")
        return redirect('admin_view_bookings')

def send_booking_status_email(booking):
    subject = f"Update on Your Booking for {booking.booking_date.strftime('%Y-%m-%d %H:%M')}"
    from_email = 'cargonepal2024@gmail.com'
    to_email = [booking.email]
    html_content = render_to_string('emails/booking_status_email.html', {'booking': booking})
    text_content = f"Hello {booking.name},\n\nYour booking status is now: {booking.get_status_display()}.\n\n"
    if booking.admin_comment:
        text_content += f"Comment: {booking.admin_comment}\n\n"
    text_content += "Thank you for choosing our service."
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()

# ---------- TESTIMONIALS ----------
@login_required
def admin_view_testimonials(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'admin/admin_view_testimonials.html', {'testimonials': testimonials})

@login_required
def admin_add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial added successfully.")
            return redirect('admin_view_testimonials')
    else:
        form = TestimonialForm()
    return render(request, 'admin/testimonial_form.html', {'form': form, 'action': 'Add'})

@login_required
def admin_update_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial updated successfully.")
            return redirect('admin_view_testimonials')
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'admin/testimonial_form.html', {'form': form, 'testimonial': testimonial, 'action': 'Update'})

@login_required
def admin_delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    if request.method == "POST":
        testimonial.delete()
        messages.success(request, "Testimonial deleted successfully.")
        return redirect('admin_view_testimonials')
    return render(request, 'admin/admin_delete_testimonial.html', {'testimonial': testimonial})

# ---------- ABOUT ----------
@login_required
def admin_about_view(request):
    about = About.objects.first()
    return render(request, 'admin/about_view.html', {'about': about})

@login_required
def edit_about(request):
    about = About.objects.first()
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, "About section updated successfully.")
            return redirect('admin_about_view')
    else:
        form = AboutForm(instance=about)
    return render(request, 'admin/about_form.html', {'form': form})

# ---------- SERVICES ----------
@login_required
def admin_services(request):
    services = Service.objects.all()
    return render(request, 'admin/service_list.html', {'services': services})

@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully.')
            return redirect('admin_services')
    else:
        form = ServiceForm()
    return render(request, 'admin/service_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('admin_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'admin/service_form.html', {'form': form, 'action': 'Edit', 'service': service})

@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully.')
        return redirect('admin_services')
    return render(request, 'admin/delete_service.html', {'service': service})

# ---------- FEATURES ----------
@login_required
def admin_features(request):
    features = Feature.objects.all()
    return render(request, 'admin/feature_list.html', {'features': features})

@login_required
def add_feature(request):
    if request.method == 'POST':
        form = FeatureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature added successfully.')
            return redirect('admin_features')
    else:
        form = FeatureForm()
    return render(request, 'admin/feature_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    if request.method == 'POST':
        form = FeatureForm(request.POST, request.FILES, instance=feature)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature updated successfully.')
            return redirect('admin_features')
    else:
        form = FeatureForm(instance=feature)
    return render(request, 'admin/feature_form.html', {'form': form, 'action': 'Edit', 'feature': feature})

@login_required
def delete_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    if request.method == 'POST':
        feature.delete()
        messages.success(request, 'Feature deleted successfully.')
        return redirect('admin_features')
    return render(request, 'admin/delete_feature.html', {'feature': feature})

# ---------- ORGANIZATION DETAILS ----------
@login_required
def admin_organization_details(request):
    organization = OrganizationInfo.objects.first()
    if not organization:
        # Optional: handle case where no record exists
        return redirect('edit_organization_details')  # or show a message
    
    context = {
        'organization': organization,
    }
    return render(request, 'admin/organization_details.html', context)

@login_required
def edit_organization_details(request):
    organization = OrganizationInfo.objects.first()
    if request.method == 'POST':
        form = OrganizationInfoForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()
            messages.success(request, "Organization details updated successfully.")
            return redirect('admin_organization_details')
    else:
        form = OrganizationInfoForm(instance=organization)
    return render(request, 'admin/organization_form.html', {'form': form, 'action': 'Edit'})

# ---------- CAROUSEL ----------
@login_required
def admin_carousel(request):
    carousel_items = CarouselItem.objects.all()
    return render(request, 'admin/carousel_list.html', {'carousel_items': carousel_items})

@login_required
def add_carousel_item(request):
    if request.method == 'POST':
        form = CarouselItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carousel item added successfully.')
            return redirect('admin_carousel')
    else:
        form = CarouselItemForm()
    return render(request, 'admin/carousel_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_carousel_item(request, pk):
    carousel_item = get_object_or_404(CarouselItem, pk=pk)
    if request.method == 'POST':
        form = CarouselItemForm(request.POST, request.FILES, instance=carousel_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carousel item updated successfully.')
            return redirect('admin_carousel')
    else:
        form = CarouselItemForm(instance=carousel_item)
    return render(request, 'admin/carousel_form.html', {'form': form, 'action': 'Edit', 'carousel_item': carousel_item})

@login_required
def delete_carousel_item(request, pk):
    carousel_item = get_object_or_404(CarouselItem, pk=pk)
    if request.method == 'POST':
        carousel_item.delete()
        messages.success(request, 'Carousel item deleted successfully.')
        return redirect('admin_carousel')
    return render(request, 'admin/delete_carousel_item.html', {'carousel_item': carousel_item})