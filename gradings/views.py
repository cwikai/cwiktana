from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Grading, GradingAttendance
from .forms import GradingForm
from members.models import Member
import json
from .models import Grading, GradingSheet, GradingSheetTemplate




# List and search scheduled gradings
def grading_list(request):
    query = request.GET.get('q', '').strip()
    gradings_qs = Grading.objects.filter(status='scheduled').order_by('-start_time')

    if query:
        gradings_qs = gradings_qs.filter(
            Q(class_name__icontains=query) |
            Q(instructor__icontains=query) |
            Q(examiner__icontains=query) |
            Q(location__icontains=query)
        )

    paginator = Paginator(gradings_qs, 10)
    page_number = request.GET.get('page')
    gradings = paginator.get_page(page_number)

    context = {
        'gradings': gradings,
        'query': query,
    }
    return render(request, 'gradings/grading_list.html', context)

@csrf_exempt
def add_grading(request):
    if request.method == 'POST':
        print("POST data:", request.POST)  # Debug: see incoming data
        form = GradingForm(request.POST)
        if form.is_valid():
            grading = form.save()
            print("Saved grading:", grading)  # Debug: confirm saved
            return JsonResponse({'success': True})
        else:
            print("Form errors:", form.errors)  # Debug: show form errors
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@require_POST
def edit_grading(request, pk):
    grading = get_object_or_404(Grading, pk=pk)
    form = GradingForm(request.POST, instance=grading)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

@require_POST
def delete_grading(request, pk):
    grading = get_object_or_404(Grading, pk=pk)
    grading.delete()
    return redirect('gradings:grading_list')

@require_POST
def complete_grading(request, pk):
    grading = get_object_or_404(Grading, pk=pk)
    grading.status = 'completed'
    grading.archived = True
    grading.save()
    return redirect('gradings:grading_list')

@require_POST
def cancel_grading(request, pk):
    grading = get_object_or_404(Grading, pk=pk)
    grading.status = 'canceled'
    grading.archived = True
    grading.save()
    return redirect('gradings:grading_list')

def get_grading_attendance(request, grading_id):
    grading = get_object_or_404(Grading, pk=grading_id)
    members = Member.objects.all()
    attendance_records = GradingAttendance.objects.filter(grading_session=grading)
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

@csrf_exempt
@require_POST
def save_grading_attendance(request, grading_id):
    grading = get_object_or_404(Grading, pk=grading_id)
    try:
        data = json.loads(request.body)
        attended_ids = data.get("attendance", [])

        GradingAttendance.objects.filter(grading_session=grading).delete()

        for member in Member.objects.all():
            present = str(member.id) in attended_ids
            GradingAttendance.objects.create(grading_session=grading, member=member, present=present)

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def grading_register(request, grading_id):
    grading = get_object_or_404(Grading, pk=grading_id)
    members = Member.objects.all()
    attendance_records = GradingAttendance.objects.filter(grading_session=grading)
    present_ids = attendance_records.filter(present=True).values_list('member_id', flat=True)

    for member in members:
        member.present = member.id in present_ids

    return render(request, 'gradings/grading_register.html', {
        'grading': grading,
        'members': members
    })

@csrf_exempt
@require_POST
def save_grading_register(request, grading_id):
    grading = get_object_or_404(Grading, pk=grading_id)
    attended_ids = request.POST.getlist("attendance")

    GradingAttendance.objects.filter(grading_session=grading).delete()

    for member in Member.objects.all():
        present = str(member.id) in attended_ids
        GradingAttendance.objects.create(grading_session=grading, member=member, present=present)

    return redirect('gradings:grading_list')

def grading_archive(request):
    query = request.GET.get("q", "")
    gradings_qs = Grading.objects.filter(status__in=["completed", "canceled"])

    if query:
        gradings_qs = gradings_qs.filter(
            Q(class_name__icontains=query) |
            Q(instructor__icontains=query)
        )

    gradings_qs = gradings_qs.order_by("-start_time")

    paginator = Paginator(gradings_qs, 10)
    page = request.GET.get("page")
    gradings = paginator.get_page(page)

    return render(request, "gradings/grading_archive.html", {
        "gradings": gradings,
        "query": query,
    })

def grading_attended(request, grading_id):
    grading = get_object_or_404(Grading, pk=grading_id)
    attendance_records = GradingAttendance.objects.filter(grading_session=grading, present=True)
    attendees = [record.member for record in attendance_records]

    return render(request, 'gradings/grading_attended.html', {
        'grading': grading,
        'attendees': attendees
    })

def manage_gradings(request):
    return render(request, 'gradings/grading_list.html')


def start_grading(request, grading_id):
    grading = get_object_or_404(Grading, id=grading_id)


    # Eventually this will be dynamic — for now, we'll show all templates (you’ll limit to active later)
    templates = GradingSheetTemplate.objects.filter(is_active=True)

    # Example: attendees linked through a ManyToManyField or attendance register
    attendees = grading.attendees.all() if hasattr(grading, 'attendees') else []

    grading_sheets = GradingSheet.objects.filter(grading=grading).select_related('template')

    context = {
        'grading': grading,
        'templates': templates,
        'grading_sheets': grading_sheets,
        'attendees': attendees,
    }
    return render(request, 'gradings/grading_sheets.html', context)