# forms.py
from django import forms
from .models import ContactMessage, Booking, BlogPost, FAQ, Testimonial
from datetime import time
from django.utils import timezone

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Message'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'booking_date', 'plan']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].widget = forms.HiddenInput()
        self.fields['booking_date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

    def clean_booking_date(self):
        booking_datetime = self.cleaned_data['booking_date']
        if booking_datetime < timezone.now():
            raise forms.ValidationError("Booking time cannot be in the past.")
        if not time(10, 0) <= booking_datetime.time() <= time(18, 0):
            raise forms.ValidationError("Bookings are allowed only between 10 AM and 6 PM.")
        return booking_datetime
    
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        exclude = ['slug', 'publish_date']

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']

class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status', 'admin_comment']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select w-50'}),
            'admin_comment': forms.Textarea(attrs={'class': 'form-control w-50', 'rows': 3}),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['customer_name', 'profession', 'content', 'image']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }