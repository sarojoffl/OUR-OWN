from django.shortcuts import render, redirect
from datetime import datetime
from .models import Booking, Service, BlogPost, ContactMessage, FAQ, Testimonial, About, Story
from .forms import BlogPostForm, FAQForm, BookingStatusForm, AboutForm, StoryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@login_required
def admin_dashboard(request):
    context = {
        'total_bookings': Booking.objects.count(),
        'total_services': Service.objects.count(),
        'total_blogs': BlogPost.objects.count(),
        'total_messages': ContactMessage.objects.count(),
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

def admin_contact_messages(request):
    contact_messages = ContactMessage.objects.order_by('-created_at')
    return render(request, 'admin/contact_messages.html', {'contact_messages': contact_messages})

def admin_delete_contact_message(request, message_id):
    message = ContactMessage.objects.get(id=message_id)
    if request.method == "POST":
        message.delete()
        messages.success(request, 'Message deleted successfully.')
        return redirect('admin_contact_messages')
    return render(request, 'admin/delete_contact_message.html', {'message': message})

def admin_add_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post added successfully.")
            return redirect('admin_view_blog_posts')
    else:
        form = BlogPostForm()
    return render(request, 'admin/add_blog_post.html', {'form': form})

def admin_view_blog_posts(request):
    posts = BlogPost.objects.order_by('-publish_date')
    return render(request, 'admin/view_blog_posts.html', {'posts': posts})

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
    return render(request, 'admin/update_blog_post.html', {'form': form, 'post': post})

def admin_delete_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Blog post deleted successfully.")
        return redirect('admin_view_blog_posts')
    return render(request, 'admin/delete_blog_post.html', {'post': post})

def admin_view_faq(request):
    return render(request, 'admin/faq.html')

def admin_view_faqs(request):
    faqs = FAQ.objects.all()
    return render(request, 'admin/faq_list.html', {'faqs': faqs})

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

def admin_delete_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == 'POST':
        faq.delete()
        messages.success(request, "FAQ deleted successfully.")
        return redirect('admin_view_faqs')
    return render(request, 'admin/faq_confirm_delete.html', {'faq': faq})

def admin_view_bookings(request):
    bookings = Booking.objects.all().order_by('-booked_on')
    return render(request, 'admin/view_bookings.html', {'bookings': bookings})

def admin_update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        form = BookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            
            # Send email notification to customer
            send_booking_status_email(booking)
            
            return redirect('admin_view_bookings')
    else:
        form = BookingStatusForm(instance=booking)
        
    return render(request, 'admin/update_booking_status.html', {'form': form, 'booking': booking})

def send_booking_status_email(booking):
    subject = f"Update on Your Booking for {booking.booking_date.strftime('%Y-%m-%d %H:%M')}"
    from_email = 'cargonepal2024@gmail.com'
    to_email = [booking.email]

    # Render HTML email content
    html_content = render_to_string('emails/booking_status_email.html', {'booking': booking})
    text_content = f"Hello {booking.name},\n\nYour booking status is now: {booking.get_status_display()}.\n\n"
    if booking.admin_comment:
        text_content += f"Comment: {booking.admin_comment}\n\n"
    text_content += "Thank you for choosing our service."

    # Compose and send the email
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()

def admin_view_testimonials(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'admin/admin_view_testimonials.html', {'testimonials': testimonials})

def admin_delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    if request.method == "POST":
        testimonial.delete()
        messages.success(request, "Testimonial deleted successfully.")
        return redirect('admin_view_testimonials')
    return render(request, 'admin/admin_delete_testimonial.html', {'testimonial': testimonial})


# ---------- ABOUT ----------
def admin_about_view(request):
    about = About.objects.first()
    return render(request, 'admin/about_view.html', {'about': about})

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


# ---------- STORY ----------
def admin_story_list(request):
    stories = Story.objects.all()
    return render(request, 'admin/story_list.html', {'stories': stories})

def add_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Story added successfully.")
            return redirect('admin_story_list')
    else:
        form = StoryForm()
    return render(request, 'admin/story_form.html', {'form': form, 'action': 'Add'})

def edit_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            messages.success(request, "Story updated successfully.")
            return redirect('admin_story_list')
    else:
        form = StoryForm(instance=story)
    return render(request, 'admin/story_form.html', {'form': form, 'action': 'Edit'})

def delete_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.method == 'POST':
        story.delete()
        messages.success(request, "Story deleted.")
        return redirect('admin_story_list')
    return render(request, 'admin/story_delete.html', {'story': story})