from django.shortcuts import render, redirect
from datetime import datetime
from .models import Booking, Service, BlogPost, ContactMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    messages = ContactMessage.objects.order_by('-id')
    return render(request, 'admin/contact_messages.html', {'messages': messages})