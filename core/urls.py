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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
