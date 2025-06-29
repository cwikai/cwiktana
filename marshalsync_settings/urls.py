from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings_page, name='settings_page'),
    path('user-login/', views.user_login_settings, name='user_login_settings'),
    path('user-management/', views.user_management, name='user_management'),
    path('roles-management/', views.roles_management, name='roles_management'),
    path('create-user-account/', views.create_user_account, name='create_user_account'),
    path('user-management/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('user-management/deactivated/', views.deactivated_users, name='deactivated_users'),
    path('user-management/reactivate/<int:user_id>/', views.reactivate_user, name='reactivate_user'),

]
