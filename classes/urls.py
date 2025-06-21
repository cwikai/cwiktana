from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('', views.classes_list, name='classes_list'),
    path('add/', views.add_class, name='add_class'),
    path('edit/<int:pk>/', views.edit_class, name='edit_class'),
    path('<int:class_id>/register/', views.class_register, name='class_register'),
    path('<int:pk>/complete/', views.complete_class, name='complete_class'),
    path('<int:pk>/cancel/', views.cancel_class, name='cancel_class'),
    path('<int:class_id>/register/save/', views.save_register, name='save_register'),
    path("archive/", views.class_archive, name="class_archive"),
    path('<int:class_id>/attended/', views.class_attended, name='class_attended'),



]
