from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import admin_views

urlpatterns = [
    # Public Views
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.services_detail, name='services_detail'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('book/', views.book_service, name='book_now'),


    # Dashboard / Admin Views
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/login/', admin_views.admin_login, name='admin_login'),
    path('dashboard/logout/', admin_views.admin_logout, name='admin_logout'),

    # Contact Messages
    path('dashboard/contact-messages/', admin_views.admin_contact_messages, name='admin_contact_messages'),
    path('dashboard/contact-messages/delete/<int:message_id>/', admin_views.admin_delete_contact_message, name='admin_delete_contact_message'),

    # Blog
    path('dashboard/blog/', admin_views.admin_view_blog_posts, name='admin_view_blog_posts'),
    path('dashboard/blog/add/', admin_views.admin_add_blog_post, name='admin_add_blog_post'),
    path('dashboard/blog/update/<int:post_id>/', admin_views.admin_update_blog_post, name='admin_update_blog_post'),
    path('dashboard/blog/delete/<int:post_id>/', admin_views.admin_delete_blog_post, name='admin_delete_blog_post'),

    # FAQ
    path('dashboard/faq/', admin_views.admin_view_faqs, name='admin_view_faqs'),
    path('dashboard/faq/add/', admin_views.admin_add_faq, name='admin_add_faq'),
    path('dashboard/faq/update/<int:faq_id>/', admin_views.admin_update_faq, name='admin_update_faq'),
    path('dashboard/faq/delete/<int:faq_id>/', admin_views.admin_delete_faq, name='admin_delete_faq'),

    # Bookings
    path('dashboard/bookings/', admin_views.admin_view_bookings, name='admin_view_bookings'),
    path('dashboard/bookings/update-status/<int:booking_id>/', admin_views.admin_update_booking_status, name='admin_update_booking_status'),

    # Testimonials
    path('dashboard/testimonials/', admin_views.admin_view_testimonials, name='admin_view_testimonials'),
    path('dashboard/testimonials/delete/<int:testimonial_id>/', admin_views.admin_delete_testimonial, name='admin_delete_testimonial'),

    # About
    path('dashboard/about/', admin_views.admin_about_view, name='admin_about_view'),
    path('dashboard/about/edit/', admin_views.edit_about, name='edit_about'),

    # Services
    path('dashboard/services/', admin_views.admin_services, name='admin_services'),
    path('dashboard/services/add/', admin_views.add_service, name='add_service'),
    path('dashboard/services/edit/<int:pk>/', admin_views.edit_service, name='edit_service'),
    path('dashboard/services/delete/<int:pk>/', admin_views.delete_service, name='delete_service'),

    # Features
    path('dashboard/features/', admin_views.admin_features, name='admin_features'),
    path('dashboard/features/add/', admin_views.add_feature, name='add_feature'),
    path('dashboard/features/edit/<int:pk>/', admin_views.edit_feature, name='edit_feature'),
    path('dashboard/features/delete/<int:pk>/', admin_views.delete_feature, name='delete_feature'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
