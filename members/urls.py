from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path("", views.members_list, name="members_list"),
    path("add/", views.add_member, name="add_member"),
    path("edit/<int:pk>/", views.edit_member, name="edit_member"),
    path("delete/<int:pk>/", views.delete_member, name="delete_member"),
]
