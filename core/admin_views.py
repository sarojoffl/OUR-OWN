from django.shortcuts import render, redirect
from datetime import datetime
from .models import Booking, Service, BlogPost, ContactMessage
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

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
