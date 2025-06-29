from django.urls import path
from .views import SupportAPIView

urlpatterns = [
    path('', SupportAPIView.as_view(), name='support_api'),
]
