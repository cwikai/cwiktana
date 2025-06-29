from django.shortcuts import render, get_object_or_404, redirect
from .models import Settings, Role
from members.models import Member
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages

def settings_page(request):
    settings = Settings.objects.all()
    return render(request, 'settings/settings_page.html', {
        'settings': settings,
    })

def user_login_settings(request):
    return render(request, 'settings/user_login_roles.html')

def user_management(request):
    users = User.objects.filter(is_active=True)
    members = Member.objects.all()
    roles = Role.objects.all()
    return render(request, 'settings/user_management.html', {
        'users': users,
        'members': members,
        'roles': roles,
    })

def roles_management(request):
    roles = Role.objects.all()
    return render(request, 'settings/roles_management.html', {'roles': roles})

@require_POST
def create_user_account(request):
    try:
        is_member = request.POST.get('is_member') == 'true'
        role_id = request.POST.get('role_id')
        new_role_name = request.POST.get('new_role_name', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        must_change_password = request.POST.get('must_change_password') == 'on'

        # Server-side password confirmation check
        if not password or not confirm_password:
            return JsonResponse({'success': False, 'error': 'Password and confirmation are required.'})
        if password != confirm_password:
            return JsonResponse({'success': False, 'error': 'Passwords do not match.'})

        # Role assignment
        role = None
        if new_role_name:
            role, created = Role.objects.get_or_create(name__iexact=new_role_name, defaults={'name': new_role_name})
            if not created:
                return JsonResponse({'success': False, 'error': f'Role "{new_role_name}" already exists. Please select it from the list.'})
        elif role_id:
            try:
                role = Role.objects.get(pk=role_id)
            except Role.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Selected role does not exist.'})

        if is_member:
            member_id = request.POST.get('member_id')
            if not member_id:
                return JsonResponse({'success': False, 'error': 'Member must be selected.'})
            try:
                member = Member.objects.get(pk=member_id)
            except Member.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Selected member does not exist.'})

            first_name = member.first_name
            last_name = member.last_name
            email = member.email
        else:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            if not all([first_name, last_name, email]):
                return JsonResponse({'success': False, 'error': 'First name, last name and email are required.'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'A user with this email already exists.'})

        # Create user
        user = User.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),
        )

        # Assign role (adjust to your actual User-Role relation)
        if role:
            user.role_set.add(role)  # Assuming M2M relation
            # or user.role = role  # if FK
            user.save()

        # Set must_change_password flag on profile
        if hasattr(user, 'profile'):
            user.profile.must_change_password = must_change_password
            user.profile.save()
        else:
            # If no profile model, you might want to create one or handle differently
            pass

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
        # Assign role (assuming ManyToMany)
        if role:
            user.role_set.add(role)

        # Save must_change_password flag on profile (adjust to your actual related model)
        if hasattr(user, 'profile'):
            user.profile.must_change_password = must_change_password
            user.profile.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_POST
def deactivate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.get_full_name()} deactivated successfully.')
    return redirect('settings:user_management')

def deactivated_users(request):
    users = User.objects.filter(is_active=False)
    return render(request, 'settings/deactivated_users.html', {
        'users': users,
    })

@require_POST
def reactivate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.get_full_name()} reactivated successfully.')
    return redirect('settings:deactivated_users')
