from django.contrib import admin
from django.urls import path, include
from . import views  # Project-level views
from accounts import views as accounts_views  # Avoid conflict
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard for logged-in users
    path("members/", include("members.urls", namespace="members")),
    path('cookies/', views.cookies, name='cookies'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('add_member/', views.add_member, name='add_member'),
    path('classes/', include('classes.urls', namespace='classes')),
    path('grading_list/', include('gradings.urls', namespace='gradings')),  # Added gradings app URLs
    path('manage_gradings/', views.manage_gradings, name='manage_gradings'),  # Optional: project-level view if still needed
    path('licenses/', views.manage_licenses, name='manage_licenses'),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
