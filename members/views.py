from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Member
from .forms import MemberForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import base64
from django.core.files.base import ContentFile
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from marshalsync_settings.models import Role



# View to list and search members
def members_list(request):
    query = request.GET.get("q", "")
    members = Member.objects.all()
    if query:
        members = members.filter(first_name__icontains=query) | members.filter(last_name__icontains=query)

    # Add role_ids list to each member
    for m in members:
        m.role_ids = list(m.roles.values_list('id', flat=True))

    paginator = Paginator(members, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "members": page_obj,
        "query": query,
        "roles": Role.objects.all(),
    }
    return render(request, "members/members_list.html", context)
# View to add a new member with optional webcam image
def add_member(request):
    if request.method == "POST":
        # Check for base64 webcam image data first
        captured_image_data = request.POST.get('profile_picture_data')  # Note the name matches your form input
        
        # Prepare a mutable copy of request.FILES (QueryDict is immutable)
        files = request.FILES.copy()
        
        if captured_image_data:
            try:
                format, imgstr = captured_image_data.split(';base64,')
                ext = format.split('/')[-1]  # e.g. 'png'
                data = ContentFile(base64.b64decode(imgstr), name='captured.%s' % ext)
                files['profile_picture'] = data
            except Exception as e:
                print("Image processing error:", e)
        
        # Now create the form using the modified files dict
        form = MemberForm(request.POST, files)

        if form.is_valid():
            member = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    "success": True,
                    "member": {
                        "id": member.pk,
                        "first_name": member.first_name,
                        "last_name": member.last_name,
                        "email": member.email,
                        "phone_number": member.phone_number,
                    }
                })
            else:
                return redirect("members:members_list")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
            else:
                return render(request, "members/members_list.html", {
                    "form": form,
                    "members": Member.objects.all()
                })
    else:
        return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

# View to edit an existing member
def edit_member(request, pk):
    member = get_object_or_404(Member, pk=pk)

    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True})
            else:
                return redirect("members:members_list")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
            else:
                # For non-AJAX, re-render edit page or members list with errors
                return render(request, "members/edit_member.html", {"form": form, "member": member})

    else:
        # GET request, show edit form
        form = MemberForm(instance=member)
        return render(request, "members/edit_member.html", {"form": form, "member": member})


# View to delete a member
def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect("members:members_list")
