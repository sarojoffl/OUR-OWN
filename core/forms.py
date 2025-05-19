# forms.py
from django import forms
from .models import ContactMessage, Booking, BlogPost, FAQ, Testimonial, About, Service, Feature, OrganizationInfo, CarouselItem
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
        fields = ['name', 'email', 'phone', 'service', 'booking_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = [
            'experience_years', 'title', 'description', 'more_info',
            'why_choose_us',
            'chairman_message', 'chairman_image', 'chairman_name',
            'md_message', 'md_image', 'md_name',
            'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'more_info': forms.Textarea(attrs={'rows': 3}),
            'why_choose_us': forms.Textarea(attrs={'rows': 3}),
            'chairman_message': forms.Textarea(attrs={'rows': 4}),
            'md_message': forms.Textarea(attrs={'rows': 4}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'image']

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['title', 'description', 'image']

class OrganizationInfoForm(forms.ModelForm):
    class Meta:
        model = OrganizationInfo
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone1': forms.TextInput(attrs={'class': 'form-control'}),
            'phone2': forms.TextInput(attrs={'class': 'form-control'}),
            'email1': forms.EmailInput(attrs={'class': 'form-control'}),
            'email2': forms.EmailInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
        }

class CarouselItemForm(forms.ModelForm):
    class Meta:
        model = CarouselItem
        fields = ['image', 'title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }