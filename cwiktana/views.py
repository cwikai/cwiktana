import logging
from django.views import View
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import subprocess
from django.contrib.auth.mixins import LoginRequiredMixin

# Configure logger for this module
logger = logging.getLogger(__name__)

# Pages
def homepage(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def manage_classes(request):
    return render(request, 'manage_classes.html')

def manage_gradings(request):
    return render(request, 'gradings/grading_list.html')

def manage_licenses(request):
    return render(request, 'manage_licenses.html')

def add_member(request):
    return render(request, 'add_member.html')

def cookies(request):
    return render(request, 'cookies.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')


