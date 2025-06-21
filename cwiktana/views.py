from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
def manage_classes(request):
    return render(request, 'manage_classes.html')
def manage_gradings(request):
    return render(request, 'grading_list.html')
def manage_licenses(request):
    return render(request, 'manage_licenses.html')





def add_member(request):
    return render(request, 'add_member.html')



def cookies(reqest):
    return render(reqest, 'cookies.html')
def privacy(reqest):
    return render(reqest, 'privacy.html')
def terms(reqest):
    return render(reqest, 'terms.html')



