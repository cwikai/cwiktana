from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import ClassSession, Attendance
from .forms import ClassSessionForm
from members.models import Member
import json

# List and search only scheduled classes
def classes_list(request):
    query = request.GET.get('q', '').strip()
    class_list = ClassSession.objects.filter(status='scheduled').order_by('-start_time')

    if query:
        class_list = class_list.filter(
            Q(class_name__icontains=query) |
            Q(instructor__icontains=query) |
            Q(location__icontains=query)
        )

    paginator = Paginator(class_list, 10)
    page_number = request.GET.get('page')
    classes = paginator.get_page(page_number)

    context = {
        'classes': classes,
        'query': query,
    }
    return render(request, 'classes/classes_list.html', context)

# Add a new class
def add_class(request):
    if request.method == 'POST':
        form = ClassSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Edit an existing class
def edit_class(request, pk):
    class_instance = get_object_or_404(ClassSession, pk=pk)
    if request.method == 'POST':
        form = ClassSessionForm(request.POST, instance=class_instance)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Delete a class
def delete_class(request, pk):
    if request.method == 'POST':
        class_instance = get_object_or_404(ClassSession, pk=pk)
        class_instance.delete()
        return redirect('classes:classes_list')
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Mark a class as completed
def complete_class(request, pk):
    if request.method == 'POST':
        class_obj = get_object_or_404(ClassSession, pk=pk)
        class_obj.status = 'completed'
        class_obj.archived = True
        class_obj.save()
        return redirect('classes:classes_list')
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Mark a class as canceled
def cancel_class(request, pk):
    if request.method == 'POST':
        class_obj = get_object_or_404(ClassSession, pk=pk)
        class_obj.status = 'canceled'
        class_obj.archived = True
        class_obj.save()
        return redirect('classes:classes_list')
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Get attendance data for a class
def get_attendance(request, class_id):
    class_session = get_object_or_404(ClassSession, pk=class_id)
    members = Member.objects.all()
    attendance_records = Attendance.objects.filter(class_session=class_session)
    present_ids = attendance_records.filter(present=True).values_list('member_id', flat=True)

    members_data = []
    for member in members:
        members_data.append({
            'id': member.id,
            'forename': member.forename,
            'surname': member.surname,
            'profile_photo': member.profile_photo.url if member.profile_photo else '/static/img/default-avatar.png',
            'present': member.id in present_ids
        })

    return JsonResponse({'members': members_data})

# Save attendance for a class
@csrf_exempt
def save_attendance(request, class_id):
    if request.method == "POST":
        class_session = get_object_or_404(ClassSession, pk=class_id)
        try:
            data = json.loads(request.body)
            attended_ids = data.get("attendance", [])

            Attendance.objects.filter(class_session=class_session).delete()

            for member in Member.objects.all():
                present = str(member.id) in attended_ids
                Attendance.objects.create(class_session=class_session, member=member, present=present)

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

# Register page for a class
def class_register(request, class_id):
    class_session = get_object_or_404(ClassSession, pk=class_id)
    members = Member.objects.all()
    attendance_records = Attendance.objects.filter(class_session=class_session)
    present_ids = attendance_records.filter(present=True).values_list('member_id', flat=True)

    for member in members:
        member.present = member.id in present_ids

    return render(request, 'classes/class_register.html', {
        'class_session': class_session,
        'members': members
    })

# Save attendance from the register page
@csrf_exempt
def save_register(request, class_id):
    if request.method == 'POST':
        class_session = get_object_or_404(ClassSession, pk=class_id)
        attended_ids = request.POST.getlist("attendance")

        Attendance.objects.filter(class_session=class_session).delete()

        for member in Member.objects.all():
            present = str(member.id) in attended_ids
            Attendance.objects.create(class_session=class_session, member=member, present=present)

        return redirect('classes:classes_list')

    return JsonResponse({'error': 'Invalid method'}, status=405)

# View archived classes (completed or canceled)
def class_archive(request):
    query = request.GET.get("q", "")
    classes = ClassSession.objects.filter(status__in=["completed", "canceled"])

    if query:
        classes = classes.filter(
            Q(class_name__icontains=query) |
            Q(instructor__icontains=query)
        )

    classes = classes.order_by("-start_time")

    paginator = Paginator(classes, 10)
    page = request.GET.get("page")
    classes = paginator.get_page(page)

    return render(request, "classes/class_archive.html", {
        "classes": classes,
        "query": query,
    })
def class_attended(request, class_id):
    class_session = get_object_or_404(ClassSession, pk=class_id)
    attendance_records = Attendance.objects.filter(class_session=class_session, present=True)
    attendees = [record.member for record in attendance_records]

    return render(request, 'classes/attended.html', {
        'class_session': class_session,
        'attendees': attendees
    })

