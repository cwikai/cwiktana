from django.urls import path
from . import views

app_name = 'gradings'

urlpatterns = [
    path('', views.grading_list, name='grading_list'),
    path('add/', views.add_grading, name='add_grading'),
    path('edit/<int:pk>/', views.edit_grading, name='edit_grading'),

    path('<int:grading_id>/register/', views.grading_register, name='grading_register'),
    path('<int:grading_id>/register/save/', views.save_grading_register, name='save_grading_register'),

    path('<int:pk>/complete/', views.complete_grading, name='complete_grading'),
    path('<int:pk>/cancel/', views.cancel_grading, name='cancel_grading'),

    path('<int:grading_id>/register/save/', views.save_grading_register, name='save_grading_register'),

    path('archive/', views.grading_archive, name='grading_archive'),
    path('<int:grading_id>/attended/', views.grading_attended, name='grading_attended'),

    # Optional: API endpoints for AJAX attendance
    path('<int:grading_id>/attendance/', views.get_grading_attendance, name='get_grading_attendance'),
    path('<int:grading_id>/attendance/save/', views.save_grading_attendance, name='save_grading_attendance'),
]
