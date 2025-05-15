from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import admin_views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.services_detail, name='services_detail'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('book-now/<int:plan_id>/', views.book_plan, name='book_now'),
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('login/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='admin_logout'),
    path('contact-messages/', admin_views.admin_contact_messages, name='admin_contact_messages'),
    path('delete-contact-message/<int:message_id>/', admin_views.admin_delete_contact_message, name='admin_delete_contact_message'),
    path('dashboard/blog/', admin_views.admin_view_blog_posts, name='admin_view_blog_posts'),
    path('dashboard/blog/add/', admin_views.admin_add_blog_post, name='admin_add_blog_post'),
    path('dashboard/blog/update/<int:post_id>/', admin_views.admin_update_blog_post, name='admin_update_blog_post'),
    path('dashboard/blog/delete/<int:post_id>/', admin_views.admin_delete_blog_post, name='admin_delete_blog_post'),
    path('dashboard/faq/', admin_views.admin_view_faqs, name='admin_view_faqs'),
    path('dashboard/faq/add/', admin_views.admin_add_faq, name='admin_add_faq'),
    path('dashboard/faq/update/<int:faq_id>/', admin_views.admin_update_faq, name='admin_update_faq'),
    path('dashboard/faq/delete/<int:faq_id>/', admin_views.admin_delete_faq, name='admin_delete_faq'),
    path('dashboard/bookings/', admin_views.admin_view_bookings, name='admin_view_bookings'),
    path('dashboard/bookings/update/<int:booking_id>/', admin_views.admin_update_booking_status, name='admin_update_booking_status'),
    path('dashboard/testimonials/', admin_views.admin_view_testimonials, name='admin_view_testimonials'),
    path('dashboard/testimonials/add/', admin_views.admin_add_testimonial, name='admin_add_testimonial'),
    path('dashboard/testimonials/update/<int:testimonial_id>/', admin_views.admin_update_testimonial, name='admin_update_testimonial'),
    path('dashboard/testimonials/delete/<int:testimonial_id>/', admin_views.admin_delete_testimonial, name='admin_delete_testimonial'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
