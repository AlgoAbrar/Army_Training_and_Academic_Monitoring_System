# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import login as auth_login, logout as auth_logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib import messages
# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods
# from django.db.models import Q, Avg, Max, Min, Count
# from django.utils import timezone
# from datetime import timedelta
# from users.models import User
# from users.forms import UserCreateForm, UserEditForm
# from soldiers.models import Soldier
# from soldiers.forms import SoldierCreateForm, SoldierEditForm
# from fitness.models import FitnessRecord
# from fitness.forms import FitnessRecordForm
# from academics.models import AcademicRecord
# from academics.forms import AcademicRecordForm
# from collections import defaultdict

# def api_root_view(request):
#     return redirect('api-root')

# def home(request):
#     return render(request, 'home.html')

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard')
    
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user)
#             messages.success(request, f'Welcome back, {user.first_name or user.username}!')
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Invalid username or password.')
#     else:
#         form = AuthenticationForm()
    
#     return render(request, 'auth/login.html', {'form': form})

# def logout_view(request):
#     auth_logout(request)
#     messages.success(request, 'You have been logged out successfully.')
#     return redirect('home')

# # @login_required
# # def dashboard(request):
# #     user = request.user
    
# #     # Debug: Print user info to console
# #     print(f"DEBUG: User: {user}")
# #     print(f"DEBUG: User attributes: {dir(user)}")
# #     print(f"DEBUG: Is authenticated: {user.is_authenticated}")
    
# #     # Safely get role with fallback
# #     try:
# #         role = user.role
# #         print(f"DEBUG: User role: {role}")
# #     except AttributeError:
# #         print("DEBUG: User has no 'role' attribute!")
# #         # If using Django's default User model, set a default role
# #         role = 'soldier'
    
# #     if role == 'admin':
# #         template = 'admin/dashboard.html'
# #     elif role == 'trainer':
# #         template = 'trainer/dashboard.html'
# #     elif role == 'teacher':
# #         template = 'teacher/dashboard.html'
# #     else:  # soldier or any other case
# #         template = 'soldier/dashboard.html'
    
# #     print(f"DEBUG: Using template: {template}")
    
# #     context = {
# #         'user': user,
# #         'role': role
# #     }
    
# #     return render(request, template, context)

# # @login_required
# # def dashboard(request):
# #     user = request.user
    
# #     # Debug information
# #     print(f"DEBUG DASHBOARD: User: {user.username}")
# #     print(f"DEBUG DASHBOARD: Authenticated: {user.is_authenticated}")
# #     print(f"DEBUG DASHBOARD: User attributes: {[attr for attr in dir(user) if not attr.startswith('_')]}")
    
# #     # Safely get role
# #     role = getattr(user, 'role', 'soldier')
# #     print(f"DEBUG DASHBOARD: User role: {role}")
    
# #     # Template mapping
# #     template_map = {
# #         'admin': 'admin/dashboard.html',
# #         'trainer': 'trainer/dashboard.html', 
# #         'teacher': 'teacher/dashboard.html',
# #         'soldier': 'soldier/dashboard.html',
# #     }
    
# #     template = template_map.get(role, 'dashboard.html')  # Fallback to generic
# #     print(f"DEBUG DASHBOARD: Using template: {template}")
    
# #     context = {
# #         'user': user,
# #         'role': role
# #     }
    
# #     try:
# #         return render(request, template, context)
# #     except:
# #         # If template doesn't exist, fallback to generic
# #         print(f"DEBUG DASHBOARD: Template {template} not found, using fallback")
# #         return render(request, 'dashboard.html', context)

# @login_required
# def dashboard(request):
#     user = request.user
#     role = getattr(user, 'role', 'soldier')
    
#     # Get counts from database
#     from users.models import User
#     from soldiers.models import Soldier
    
#     context = {
#         'user': user,
#         'role': role,
#         'total_users': User.objects.count(),
#         'total_soldiers': Soldier.objects.count(),
#         'total_trainers': User.objects.filter(role='trainer').count(),
#         'total_teachers': User.objects.filter(role='teacher').count(),
#     }
    
#     template_map = {
#         'admin': 'admin/dashboard.html',
#         'trainer': 'trainer/dashboard.html', 
#         'teacher': 'teacher/dashboard.html',
#         'soldier': 'soldier/dashboard.html',
#     }
    
#     template = template_map.get(role, 'dashboard.html')
    
#     return render(request, template, context)


# # ... existing views ...

# @login_required
# def user_management(request):
#     """User management dashboard for admin"""
#     if request.user.role != 'admin':
#         messages.error(request, 'Access denied. Admin privileges required.')
#         return redirect('dashboard')
    
#     users = User.objects.all().order_by('-date_joined')
    
#     context = {
#         'users': users,
#         'total_users': users.count(),
#         'active_users': users.filter(is_active=True).count(),
#         'admins': users.filter(role='admin').count(),
#         'trainers': users.filter(role='trainer').count(),
#         'teachers': users.filter(role='teacher').count(),
#         'soldiers': users.filter(role='soldier').count(),
#     }
    
#     return render(request, 'admin/user_management.html', context)

# @login_required
# def create_user(request):
#     """Create new user"""
#     if request.user.role != 'admin':
#         messages.error(request, 'Access denied. Admin privileges required.')
#         return redirect('dashboard')
    
#     if request.method == 'POST':
#         form = UserCreateForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, f'User {user.username} created successfully!')
#             return redirect('user_management')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = UserCreateForm()
    
#     return render(request, 'admin/user_form.html', {
#         'form': form,
#         'title': 'Create New User',
#         'submit_text': 'Create User'
#     })

# @login_required
# def edit_user(request, user_id):
#     """Edit existing user"""
#     if request.user.role != 'admin':
#         messages.error(request, 'Access denied. Admin privileges required.')
#         return redirect('dashboard')
    
#     user = get_object_or_404(User, id=user_id)
    
#     if request.method == 'POST':
#         form = UserEditForm(request.POST, instance=user)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, f'User {user.username} updated successfully!')
#             return redirect('user_management')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = UserEditForm(instance=user)
    
#     return render(request, 'admin/user_form.html', {
#         'form': form,
#         'title': f'Edit User: {user.username}',
#         'submit_text': 'Update User',
#         'user': user
#     })

# @login_required
# @require_http_methods(["POST"])
# def toggle_user_status(request, user_id):
#     """Activate/Deactivate user"""
#     if request.user.role != 'admin':
#         return JsonResponse({'error': 'Access denied'}, status=403)
    
#     user = get_object_or_404(User, id=user_id)
    
#     # Prevent self-deactivation
#     if user == request.user:
#         return JsonResponse({'error': 'Cannot deactivate your own account'}, status=400)
    
#     user.is_active = not user.is_active
#     user.save()
    
#     action = 'activated' if user.is_active else 'deactivated'
#     return JsonResponse({
#         'success': True,
#         'message': f'User {user.username} {action} successfully',
#         'is_active': user.is_active
#     })

# @login_required
# @require_http_methods(["POST"])
# def delete_user(request, user_id):
#     """Delete user"""
#     if request.user.role != 'admin':
#         return JsonResponse({'error': 'Access denied'}, status=403)
    
#     user = get_object_or_404(User, id=user_id)
    
#     # Prevent self-deletion
#     if user == request.user:
#         return JsonResponse({'error': 'Cannot delete your own account'}, status=400)
    
#     username = user.username
#     user.delete()
    
#     return JsonResponse({
#         'success': True,
#         'message': f'User {username} deleted successfully'
#     })
    
# @login_required
# def soldier_management(request):
#     """Soldier management dashboard for trainers and admins"""
#     if request.user.role not in ['admin', 'trainer']:
#         messages.error(request, 'Access denied. Trainer or Admin privileges required.')
#         return redirect('dashboard')
    
#     # Filter soldiers based on user role
#     if request.user.role == 'admin':
#         soldiers = Soldier.objects.all().select_related('user', 'assigned_trainer')
#     else:  # trainer
#         soldiers = Soldier.objects.filter(assigned_trainer=request.user).select_related('user', 'assigned_trainer')
    
#     # Get search parameters
#     search_query = request.GET.get('search', '')
#     rank_filter = request.GET.get('rank', '')
#     unit_filter = request.GET.get('unit', '')
    
#     # Apply filters
#     if search_query:
#         soldiers = soldiers.filter(
#             Q(user__first_name__icontains=search_query) |
#             Q(user__last_name__icontains=search_query) |
#             Q(soldier_id__icontains=search_query) |
#             Q(unit__icontains=search_query)
#         )
    
#     if rank_filter:
#         soldiers = soldiers.filter(rank=rank_filter)
    
#     if unit_filter:
#         soldiers = soldiers.filter(unit__icontains=unit_filter)
    
#     soldiers = soldiers.order_by('-created_at')
    
#     # Get unique ranks and units for filters
#     ranks = Soldier.RANK_CHOICES
#     units = Soldier.objects.values_list('unit', flat=True).distinct()
    
#     context = {
#         'soldiers': soldiers,
#         'total_soldiers': soldiers.count(),
#         'ranks': ranks,
#         'units': units,
#         'search_query': search_query,
#         'rank_filter': rank_filter,
#         'unit_filter': unit_filter,
#     }
    
#     return render(request, 'trainer/soldier_management.html', context)

# @login_required
# def create_soldier(request):
#     """Create new soldier"""
#     if request.user.role not in ['admin', 'trainer']:
#         messages.error(request, 'Access denied. Trainer or Admin privileges required.')
#         return redirect('dashboard')
    
#     if request.method == 'POST':
#         form = SoldierCreateForm(request.user, request.POST)
#         if form.is_valid():
#             soldier = form.save()
#             messages.success(request, f'Soldier {soldier.user.get_full_name()} created successfully!')
#             return redirect('soldier_management')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = SoldierCreateForm(request.user)
    
#     return render(request, 'trainer/soldier_form.html', {
#         'form': form,
#         'title': 'Create New Soldier',
#         'submit_text': 'Create Soldier'
#     })

# @login_required
# def edit_soldier(request, soldier_id):
#     """Edit existing soldier"""
#     if request.user.role not in ['admin', 'trainer']:
#         messages.error(request, 'Access denied. Trainer or Admin privileges required.')
#         return redirect('dashboard')
    
#     soldier = get_object_or_404(Soldier, id=soldier_id)
    
#     # Check if trainer is allowed to edit this soldier
#     if request.user.role == 'trainer' and soldier.assigned_trainer != request.user:
#         messages.error(request, 'Access denied. You can only edit soldiers assigned to you.')
#         return redirect('soldier_management')
    
#     if request.method == 'POST':
#         form = SoldierEditForm(request.user, request.POST, instance=soldier)
#         if form.is_valid():
#             soldier = form.save()
#             messages.success(request, f'Soldier {soldier.user.get_full_name()} updated successfully!')
#             return redirect('soldier_management')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = SoldierEditForm(request.user, instance=soldier)
    
#     return render(request, 'trainer/soldier_form.html', {
#         'form': form,
#         'title': f'Edit Soldier: {soldier.user.get_full_name()}',
#         'submit_text': 'Update Soldier',
#         'soldier': soldier
#     })

# @login_required
# def soldier_detail(request, soldier_id):
#     """View soldier details"""
#     if request.user.role not in ['admin', 'trainer']:
#         messages.error(request, 'Access denied. Trainer or Admin privileges required.')
#         return redirect('dashboard')
    
#     soldier = get_object_or_404(Soldier, id=soldier_id)
    
#     # Check if trainer is allowed to view this soldier
#     if request.user.role == 'trainer' and soldier.assigned_trainer != request.user:
#         messages.error(request, 'Access denied. You can only view soldiers assigned to you.')
#         return redirect('soldier_management')
    
#     # Get fitness and academic records
#     from fitness.models import FitnessRecord
#     from academics.models import AcademicRecord
    
#     fitness_records = FitnessRecord.objects.filter(soldier=soldier).order_by('-date')[:5]
#     academic_records = AcademicRecord.objects.filter(soldier=soldier).order_by('-created_at')[:5]
    
#     context = {
#         'soldier': soldier,
#         'fitness_records': fitness_records,
#         'academic_records': academic_records,
#     }
    
#     return render(request, 'trainer/soldier_detail.html', context)

# # @login_required
# # def soldier_detail(request, soldier_id):
# #     """View soldier details"""
# #     if request.user.role not in ['admin', 'trainer']:
# #         messages.error(request, 'Access denied. Trainer or Admin privileges required.')
# #         return redirect('dashboard')
    
# #     soldier = get_object_or_404(Soldier, id=soldier_id)
    
# #     # Check if trainer is allowed to view this soldier
# #     if request.user.role == 'trainer' and soldier.assigned_trainer != request.user:
# #         messages.error(request, 'Access denied. You can only view soldiers assigned to you.')
# #         return redirect('soldier_management')
    
# #     # Get fitness and academic records
# #     from fitness.models import FitnessRecord
# #     from academics.models import AcademicRecord
    
# #     fitness_records = FitnessRecord.objects.filter(soldier=soldier).order_by('-date')[:5]
# #     academic_records = AcademicRecord.objects.filter(soldier=soldier).order_by('-created_at')[:5]
    
# #     # Calculate service duration
# #     from datetime import date
# #     today = date.today()
# #     joining_date = soldier.joining_date
    
# #     years = today.year - joining_date.year
# #     months = today.month - joining_date.month
    
# #     if today.day < joining_date.day:
# #         months -= 1
    
# #     if months < 0:
# #         years -= 1
# #         months += 12
    
# #     service_duration = f"{years} year{'s' if years != 1 else ''}"
# #     if months > 0:
# #         service_duration += f" {months} month{'s' if months != 1 else ''}"
    
# #     context = {
# #         'soldier': soldier,
# #         'fitness_records': fitness_records,
# #         'academic_records': academic_records,
# #         'service_duration': service_duration,
# #     }
    
# #     return render(request, 'trainer/soldier_detail.html', context)

# @login_required
# @require_http_methods(["POST"])
# def delete_soldier(request, soldier_id):
#     """Delete soldier"""
#     if request.user.role not in ['admin', 'trainer']:
#         return JsonResponse({'error': 'Access denied'}, status=403)
    
#     soldier = get_object_or_404(Soldier, id=soldier_id)
    
#     # Check if trainer is allowed to delete this soldier
#     if request.user.role == 'trainer' and soldier.assigned_trainer != request.user:
#         return JsonResponse({'error': 'Access denied. You can only delete soldiers assigned to you.'}, status=403)
    
#     soldier_name = soldier.user.get_full_name()
#     soldier_id_str = soldier.soldier_id
    
#     # Delete the soldier (this will not delete the user)
#     soldier.delete()
    
#     return JsonResponse({
#         'success': True,
#         'message': f'Soldier {soldier_name} ({soldier_id_str}) deleted successfully'
#     })
    
# @login_required
# def fitness_records(request):
#     """Fitness records management for trainers and admins"""
#     if request.user.role not in ['admin', 'trainer']:
#         messages.error(request, 'Access denied. Trainer or Admin privileges required.')
#         return redirect('dashboard')
    
#     # Filter records based on user role
#     if request.user.role == 'admin':
#         records = FitnessRecord.objects.all().select_related('soldier__user', 'created_by')
#     else:  # trainer
#         records = FitnessRecord.objects.filter(
#             Q(soldier__assigned_trainer=request.user) | Q(created_by=request.user)
#         ).select_related('soldier__user', 'created_by')
    
#     # Get filter parameters
#     soldier_filter = request.GET.get('soldier', '')
#     date_from = request.GET.get('date_from', '')
#     date_to = request.GET.get('date_to', '')
    
#     # Apply filters
#     if soldier_filter:
#         records = records.filter(soldier_id=soldier_filter)
    
#     if date_from:
#         records = records.filter(date__gte=date_from)
    
#     if date_to:
#         records = records.filter(date__lte=date_to)
    
#     records = records.order_by('-date', '-created_at')
    
#     # Get soldiers for filter dropdown
#     if request.user.role == 'admin':
#         soldiers = Soldier.objects.all().select_related('user')
#     else:
#         soldiers = Soldier.objects.filter(assigned_trainer=request.user).select_related('user')
    
#     # Calculate some statistics
#     total_records = records.count()
#     if total_records > 0:
#         avg_pushups = records.aggregate(Avg('pushups'))['pushups__avg'] or 0
#         avg_running = records.aggregate(Avg('running_distance'))['running_distance__avg'] or 0
#         avg_accuracy = records.aggregate(Avg('shooting_accuracy'))['shooting_accuracy__avg'] or 0
#     else:
#         avg_pushups = avg_running = avg_accuracy = 0
    
#     context = {
#         'records': records,
#         'soldiers': soldiers,
#         'total_records': total_records,
#         'avg_pushups': round(avg_pushups, 1),
#         'avg_running': round(avg_running, 2),
#         'avg_accuracy': round(avg_accuracy, 1),
#         'soldier_filter': soldier_filter,
#         'date_from': date_from,
#         'date_to': date_to,
#     }
    
#     return render(request, 'trainer/fitness_records.html', context)

# @login_required
# def create_fitness_record(request):
#     """Create new fitness record"""
#     if request.user.role not in ['admin', 'trainer']:
#         messages.error(request, 'Access denied. Trainer or Admin privileges required.')
#         return redirect('dashboard')
    
#     if request.method == 'POST':
#         form = FitnessRecordForm(request.user, request.POST)
#         if form.is_valid():
#             fitness_record = form.save(commit=False)
#             fitness_record.created_by = request.user
#             fitness_record.save()
            
#             messages.success(request, f'Fitness record for {fitness_record.soldier.user.get_full_name()} created successfully!')
#             return redirect('fitness_records')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = FitnessRecordForm(request.user)
    
#     return render(request, 'trainer/fitness_form.html', {
#         'form': form,
#         'title': 'Create Fitness Record',
#         'submit_text': 'Create Record'
#     })

# @login_required
# def edit_fitness_record(request, record_id):
#     """Edit existing fitness record"""
#     if request.user.role not in ['admin', 'trainer']:
#         messages.error(request, 'Access denied. Trainer or Admin privileges required.')
#         return redirect('dashboard')
    
#     record = get_object_or_404(FitnessRecord, id=record_id)
    
#     # Check permissions
#     if request.user.role == 'trainer' and record.soldier.assigned_trainer != request.user and record.created_by != request.user:
#         messages.error(request, 'Access denied. You can only edit records for your assigned soldiers.')
#         return redirect('fitness_records')
    
#     if request.method == 'POST':
#         form = FitnessRecordForm(request.user, request.POST, instance=record)
#         if form.is_valid():
#             fitness_record = form.save()
#             messages.success(request, f'Fitness record for {fitness_record.soldier.user.get_full_name()} updated successfully!')
#             return redirect('fitness_records')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = FitnessRecordForm(request.user, instance=record)
    
#     return render(request, 'trainer/fitness_form.html', {
#         'form': form,
#         'title': f'Edit Fitness Record - {record.soldier.user.get_full_name()}',
#         'submit_text': 'Update Record',
#         'record': record
#     })

# @login_required
# def fitness_record_detail(request, record_id):
#     """View fitness record details"""
#     if request.user.role not in ['admin', 'trainer']:
#         messages.error(request, 'Access denied. Trainer or Admin privileges required.')
#         return redirect('dashboard')
    
#     record = get_object_or_404(FitnessRecord, id=record_id)
    
#     # Check permissions
#     if request.user.role == 'trainer' and record.soldier.assigned_trainer != request.user and record.created_by != request.user:
#         messages.error(request, 'Access denied. You can only view records for your assigned soldiers.')
#         return redirect('fitness_records')
    
#     # Get performance evaluation
#     performance = record.evaluate_performance()
    
#     context = {
#         'record': record,
#         'performance': performance,
#     }
    
#     return render(request, 'trainer/fitness_detail.html', context)

# @login_required
# @require_http_methods(["POST"])
# def delete_fitness_record(request, record_id):
#     """Delete fitness record"""
#     if request.user.role not in ['admin', 'trainer']:
#         return JsonResponse({'error': 'Access denied'}, status=403)
    
#     record = get_object_or_404(FitnessRecord, id=record_id)
    
#     # Check permissions
#     if request.user.role == 'trainer' and record.soldier.assigned_trainer != request.user and record.created_by != request.user:
#         return JsonResponse({'error': 'Access denied. You can only delete records for your assigned soldiers.'}, status=403)
    
#     soldier_name = record.soldier.user.get_full_name()
#     record_date = record.date
    
#     record.delete()
    
#     return JsonResponse({
#         'success': True,
#         'message': f'Fitness record for {soldier_name} on {record_date} deleted successfully'
#     })

# @login_required
# def soldier_fitness_history(request, soldier_id):
#     """View fitness history for a specific soldier"""
#     if request.user.role not in ['admin', 'trainer']:
#         messages.error(request, 'Access denied. Trainer or Admin privileges required.')
#         return redirect('dashboard')
    
#     soldier = get_object_or_404(Soldier, id=soldier_id)
    
#     # Check permissions
#     if request.user.role == 'trainer' and soldier.assigned_trainer != request.user:
#         messages.error(request, 'Access denied. You can only view fitness history for your assigned soldiers.')
#         return redirect('fitness_records')
    
#     records = FitnessRecord.objects.filter(soldier=soldier).order_by('-date')
    
#     # Calculate statistics
#     if records.exists():
#         stats = records.aggregate(
#             avg_pushups=Avg('pushups'),
#             avg_running_distance=Avg('running_distance'),
#             avg_running_time=Avg('running_time'),
#             avg_bmi=Avg('bmi'),
#             avg_shooting_accuracy=Avg('shooting_accuracy'),
#             max_pushups=Max('pushups'),
#             max_running_distance=Max('running_distance'),
#             min_running_time=Min('running_time'),
#             max_shooting_accuracy=Max('shooting_accuracy'),
#         )
        
#         # Calculate progress (latest vs oldest record)
#         latest_record = records.first()
#         oldest_record = records.last()
        
#         progress = {
#             'pushups': latest_record.pushups - oldest_record.pushups,
#             'running_distance': latest_record.running_distance - oldest_record.running_distance,
#             'running_time': oldest_record.running_time - latest_record.running_time,  # Lower time is better
#             'shooting_accuracy': latest_record.shooting_accuracy - oldest_record.shooting_accuracy,
#         }
#     else:
#         stats = {}
#         progress = {}
    
#     context = {
#         'soldier': soldier,
#         'records': records,
#         'stats': stats,
#         'progress': progress,
#         'total_records': records.count(),
#     }
    
#     return render(request, 'trainer/soldier_fitness_history.html', context)

# @login_required
# def academic_records(request):
#     """Academic records management for teachers and admins"""
#     if request.user.role not in ['admin', 'teacher']:
#         messages.error(request, 'Access denied. Teacher or Admin privileges required.')
#         return redirect('dashboard')
    
#     # Filter records based on user role
#     if request.user.role == 'admin':
#         records = AcademicRecord.objects.all().select_related('soldier__user', 'created_by')
#     else:  # teacher
#         records = AcademicRecord.objects.filter(created_by=request.user).select_related('soldier__user', 'created_by')
    
#     # Get filter parameters
#     soldier_filter = request.GET.get('soldier', '')
#     subject_filter = request.GET.get('subject', '')
#     exam_filter = request.GET.get('exam', '')
#     date_from = request.GET.get('date_from', '')
#     date_to = request.GET.get('date_to', '')
    
#     # Apply filters
#     if soldier_filter:
#         records = records.filter(soldier_id=soldier_filter)
    
#     if subject_filter:
#         records = records.filter(subject=subject_filter)
    
#     if exam_filter:
#         records = records.filter(exam_name__icontains=exam_filter)
    
#     if date_from:
#         records = records.filter(created_at__date__gte=date_from)
    
#     if date_to:
#         records = records.filter(created_at__date__lte=date_to)
    
#     records = records.order_by('-created_at')
    
#     # Get soldiers and subjects for filter dropdowns
#     if request.user.role == 'admin':
#         soldiers = Soldier.objects.all().select_related('user')
#     else:
#         # Teachers can see all soldiers for academic records
#         soldiers = Soldier.objects.all().select_related('user')
    
#     subjects = AcademicRecord.SUBJECT_CHOICES
#     exam_names = AcademicRecord.objects.values_list('exam_name', flat=True).distinct()
    
#     # Calculate statistics
#     total_records = records.count()
#     if total_records > 0:
#         avg_marks = records.aggregate(Avg('marks'))['marks__avg'] or 0
#         avg_percentage = records.aggregate(Avg('percentage'))['percentage__avg'] or 0
#         top_performer = records.order_by('-percentage').first()
#     else:
#         avg_marks = avg_percentage = 0
#         top_performer = None
    
#     context = {
#         'records': records,
#         'soldiers': soldiers,
#         'subjects': subjects,
#         'exam_names': exam_names,
#         'total_records': total_records,
#         'avg_marks': round(avg_marks, 1),
#         'avg_percentage': round(avg_percentage, 1),
#         'top_performer': top_performer,
#         'soldier_filter': soldier_filter,
#         'subject_filter': subject_filter,
#         'exam_filter': exam_filter,
#         'date_from': date_from,
#         'date_to': date_to,
#     }
    
#     return render(request, 'teacher/academic_records.html', context)

# @login_required
# def create_academic_record(request):
#     """Create new academic record"""
#     if request.user.role not in ['admin', 'teacher']:
#         messages.error(request, 'Access denied. Teacher or Admin privileges required.')
#         return redirect('dashboard')
    
#     if request.method == 'POST':
#         form = AcademicRecordForm(request.user, request.POST)
#         if form.is_valid():
#             academic_record = form.save(commit=False)
#             academic_record.created_by = request.user
#             academic_record.save()
            
#             messages.success(request, f'Academic record for {academic_record.soldier.user.get_full_name()} created successfully!')
#             return redirect('academic_records')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = AcademicRecordForm(request.user)
    
#     return render(request, 'teacher/academic_form.html', {
#         'form': form,
#         'title': 'Create Academic Record',
#         'submit_text': 'Create Record'
#     })

# @login_required
# def edit_academic_record(request, record_id):
#     """Edit existing academic record"""
#     if request.user.role not in ['admin', 'teacher']:
#         messages.error(request, 'Access denied. Teacher or Admin privileges required.')
#         return redirect('dashboard')
    
#     record = get_object_or_404(AcademicRecord, id=record_id)
    
#     # Check permissions
#     if request.user.role == 'teacher' and record.created_by != request.user:
#         messages.error(request, 'Access denied. You can only edit records created by you.')
#         return redirect('academic_records')
    
#     if request.method == 'POST':
#         form = AcademicRecordForm(request.user, request.POST, instance=record)
#         if form.is_valid():
#             academic_record = form.save()
#             messages.success(request, f'Academic record for {academic_record.soldier.user.get_full_name()} updated successfully!')
#             return redirect('academic_records')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = AcademicRecordForm(request.user, instance=record)
    
#     return render(request, 'teacher/academic_form.html', {
#         'form': form,
#         'title': f'Edit Academic Record - {record.soldier.user.get_full_name()}',
#         'submit_text': 'Update Record',
#         'record': record
#     })

# @login_required
# def academic_record_detail(request, record_id):
#     """View academic record details"""
#     if request.user.role not in ['admin', 'teacher']:
#         messages.error(request, 'Access denied. Teacher or Admin privileges required.')
#         return redirect('dashboard')
    
#     record = get_object_or_404(AcademicRecord, id=record_id)
    
#     # Check permissions
#     if request.user.role == 'teacher' and record.created_by != request.user:
#         messages.error(request, 'Access denied. You can only view records created by you.')
#         return redirect('academic_records')
    
#     # Get performance evaluation
#     performance = record.evaluate_performance()
    
#     context = {
#         'record': record,
#         'performance': performance,
#     }
    
#     return render(request, 'teacher/academic_detail.html', context)

# @login_required
# @require_http_methods(["POST"])
# def delete_academic_record(request, record_id):
#     """Delete academic record"""
#     if request.user.role not in ['admin', 'teacher']:
#         return JsonResponse({'error': 'Access denied'}, status=403)
    
#     record = get_object_or_404(AcademicRecord, id=record_id)
    
#     # Check permissions
#     if request.user.role == 'teacher' and record.created_by != request.user:
#         return JsonResponse({'error': 'Access denied. You can only delete records created by you.'}, status=403)
    
#     soldier_name = record.soldier.user.get_full_name()
#     exam_name = record.exam_name
    
#     record.delete()
    
#     return JsonResponse({
#         'success': True,
#         'message': f'Academic record for {soldier_name} ({exam_name}) deleted successfully'
#     })

# @login_required
# def soldier_academic_history(request, soldier_id):
#     """View academic history for a specific soldier"""
#     if request.user.role not in ['admin', 'teacher']:
#         messages.error(request, 'Access denied. Teacher or Admin privileges required.')
#         return redirect('dashboard')
    
#     soldier = get_object_or_404(Soldier, id=soldier_id)
    
#     records = AcademicRecord.objects.filter(soldier=soldier).order_by('-created_at')
    
#     # Calculate statistics
#     if records.exists():
#         stats = records.aggregate(
#             avg_marks=Avg('marks'),
#             avg_percentage=Avg('percentage'),
#             max_marks=Max('marks'),
#             max_percentage=Max('percentage'),
#             total_exams=Count('id'),
#             distinct_subjects=Count('subject', distinct=True)
#         )
        
#         # Subject-wise performance
#         subject_stats = records.values('subject').annotate(
#             avg_marks=Avg('marks'),
#             avg_percentage=Avg('percentage'),
#             count=Count('id')
#         ).order_by('-avg_percentage')
        
#         # Progress (latest vs average)
#         latest_record = records.first()
#         overall_avg = stats['avg_percentage'] or 0
#         progress = latest_record.percentage - overall_avg if latest_record else 0
#     else:
#         stats = {}
#         subject_stats = []
#         progress = 0
    
#     context = {
#         'soldier': soldier,
#         'records': records,
#         'stats': stats,
#         'subject_stats': subject_stats,
#         'progress': progress,
#         'total_records': records.count(),
#     }
    
#     return render(request, 'teacher/soldier_academic_history.html', context)

# @login_required
# def subject_analytics(request):
#     """View analytics by subject"""
#     if request.user.role not in ['admin', 'teacher']:
#         messages.error(request, 'Access denied. Teacher or Admin privileges required.')
#         return redirect('dashboard')
    
#     # Filter records based on user role
#     if request.user.role == 'admin':
#         records = AcademicRecord.objects.all()
#     else:  # teacher
#         records = AcademicRecord.objects.filter(created_by=request.user)
    
#     # Subject-wise analytics
#     subject_analytics = records.values('subject').annotate(
#         total_students=Count('soldier', distinct=True),
#         total_exams=Count('id'),
#         avg_marks=Avg('marks'),
#         avg_percentage=Avg('percentage'),
#         max_percentage=Max('percentage'),
#         min_percentage=Min('percentage')
#     ).order_by('-avg_percentage')
    
#     # Overall statistics
#     total_students = Soldier.objects.count()
#     total_records = records.count()
#     overall_avg_percentage = records.aggregate(Avg('percentage'))['percentage__avg'] or 0
    
#     context = {
#         'subject_analytics': subject_analytics,
#         'total_students': total_students,
#         'total_records': total_records,
#         'overall_avg_percentage': round(overall_avg_percentage, 1),
#     }
    
#     return render(request, 'teacher/subject_analytics.html', context)

# @login_required
# def dashboard(request):
#     user = request.user
#     role = getattr(user, 'role', 'soldier')
    
#     # Get analytics data based on user role
#     analytics_data = get_dashboard_analytics(request.user)
    
#     context = {
#         'user': user,
#         'role': role,
#         'analytics': analytics_data,
#     }
    
#     template_map = {
#         'admin': 'admin/dashboard.html',
#         'trainer': 'trainer/dashboard.html', 
#         'teacher': 'teacher/dashboard.html',
#         'soldier': 'soldier/dashboard.html',
#     }
    
#     template = template_map.get(role, 'dashboard.html')
    
#     return render(request, template, context)

# def get_dashboard_analytics(user):
#     """Get analytics data for dashboard based on user role"""
#     analytics = {}
    
#     if user.role == 'admin':
#         analytics = get_admin_analytics()
#     elif user.role == 'trainer':
#         analytics = get_trainer_analytics(user)
#     elif user.role == 'teacher':
#         analytics = get_teacher_analytics(user)
#     else:  # soldier
#         analytics = get_soldier_analytics(user)
    
#     return analytics

# def get_admin_analytics():
#     """Admin dashboard analytics"""
#     from users.models import User
#     from soldiers.models import Soldier
#     from fitness.models import FitnessRecord
#     from academics.models import AcademicRecord
    
#     # User statistics
#     total_users = User.objects.count()
#     users_by_role = User.objects.values('role').annotate(count=Count('id'))
    
#     # Soldier statistics
#     total_soldiers = Soldier.objects.count()
#     soldiers_by_rank = Soldier.objects.values('rank').annotate(count=Count('id'))
    
#     # Fitness statistics
#     fitness_records = FitnessRecord.objects.all()
#     total_fitness_records = fitness_records.count()
#     avg_pushups = fitness_records.aggregate(avg=Avg('pushups'))['avg'] or 0
#     avg_running = fitness_records.aggregate(avg=Avg('running_distance'))['avg'] or 0
    
#     # Academic statistics
#     academic_records = AcademicRecord.objects.all()
#     total_academic_records = academic_records.count()
#     avg_percentage = academic_records.aggregate(avg=Avg('percentage'))['avg'] or 0
    
#     # Recent activity (last 7 days)
#     week_ago = timezone.now() - timedelta(days=7)
#     recent_users = User.objects.filter(date_joined__gte=week_ago).count()
#     recent_fitness = FitnessRecord.objects.filter(created_at__gte=week_ago).count()
#     recent_academics = AcademicRecord.objects.filter(created_at__gte=week_ago).count()
    
#     # Performance trends (last 30 days)
#     month_ago = timezone.now() - timedelta(days=30)
#     fitness_trend = FitnessRecord.objects.filter(
#         created_at__gte=month_ago
#     ).extra({
#         'date': "date(created_at)"
#     }).values('date').annotate(
#         count=Count('id'),
#         avg_pushups=Avg('pushups'),
#         avg_running=Avg('running_distance')
#     ).order_by('date')
    
#     academic_trend = AcademicRecord.objects.filter(
#         created_at__gte=month_ago
#     ).extra({
#         'date': "date(created_at)"
#     }).values('date').annotate(
#         count=Count('id'),
#         avg_percentage=Avg('percentage')
#     ).order_by('date')
    
#     return {
#         'total_users': total_users,
#         'users_by_role': list(users_by_role),
#         'total_soldiers': total_soldiers,
#         'soldiers_by_rank': list(soldiers_by_rank),
#         'total_fitness_records': total_fitness_records,
#         'avg_pushups': round(avg_pushups, 1),
#         'avg_running': round(avg_running, 2),
#         'total_academic_records': total_academic_records,
#         'avg_percentage': round(avg_percentage, 1),
#         'recent_activity': {
#             'users': recent_users,
#             'fitness': recent_fitness,
#             'academics': recent_academics,
#         },
#         'fitness_trend': list(fitness_trend),
#         'academic_trend': list(academic_trend),
#     }

# def get_trainer_analytics(user):
#     """Trainer dashboard analytics"""
#     from soldiers.models import Soldier
#     from fitness.models import FitnessRecord
    
#     # Soldier statistics
#     assigned_soldiers = Soldier.objects.filter(assigned_trainer=user)
#     total_soldiers = assigned_soldiers.count()
    
#     # Fitness statistics for assigned soldiers
#     fitness_records = FitnessRecord.objects.filter(soldier__assigned_trainer=user)
#     total_records = fitness_records.count()
    
#     if total_records > 0:
#         avg_pushups = fitness_records.aggregate(avg=Avg('pushups'))['avg'] or 0
#         avg_running = fitness_records.aggregate(avg=Avg('running_distance'))['avg'] or 0
#         avg_accuracy = fitness_records.aggregate(avg=Avg('shooting_accuracy'))['avg'] or 0
        
#         # Performance distribution
#         performance_data = []
#         for record in fitness_records:
#             performance = record.evaluate_performance()
#             performance_data.append(performance['overall'])
        
#         from collections import Counter
#         performance_dist = Counter(performance_data)
#     else:
#         avg_pushups = avg_running = avg_accuracy = 0
#         performance_dist = {}
    
#     # Recent records (last 7 days)
#     week_ago = timezone.now() - timedelta(days=7)
#     recent_records = fitness_records.filter(created_at__gte=week_ago).count()
    
#     # Top performers
#     top_performers = assigned_soldiers.annotate(
#         avg_pushups=Avg('fitness_records__pushups'),
#         avg_running=Avg('fitness_records__running_distance'),
#         record_count=Count('fitness_records')
#     ).filter(record_count__gt=0).order_by('-avg_pushups')[:5]
    
#     # Monthly progress
#     monthly_data = fitness_records.filter(
#         created_at__gte=timezone.now() - timedelta(days=30)
#     ).extra({
#         'week': "strftime('%%Y-%%W', created_at)"
#     }).values('week').annotate(
#         avg_pushups=Avg('pushups'),
#         avg_running=Avg('running_distance'),
#         count=Count('id')
#     ).order_by('week')
    
#     return {
#         'total_soldiers': total_soldiers,
#         'total_records': total_records,
#         'avg_pushups': round(avg_pushups, 1),
#         'avg_running': round(avg_running, 2),
#         'avg_accuracy': round(avg_accuracy, 1),
#         'performance_distribution': dict(performance_dist),
#         'recent_records': recent_records,
#         'top_performers': list(top_performers),
#         'monthly_data': list(monthly_data),
#     }

# def get_teacher_analytics(user):
#     """Teacher dashboard analytics"""
#     from academics.models import AcademicRecord
#     from soldiers.models import Soldier
    
#     # Academic statistics
#     academic_records = AcademicRecord.objects.filter(created_by=user)
#     total_records = academic_records.count()
    
#     if total_records > 0:
#         avg_marks = academic_records.aggregate(avg=Avg('marks'))['avg'] or 0
#         avg_percentage = academic_records.aggregate(avg=Avg('percentage'))['avg'] or 0
        
#         # Grade distribution
#         grade_data = []
#         for record in academic_records:
#             grade_data.append(record.grade)
        
#         from collections import Counter
#         grade_dist = Counter(grade_data)
        
#         # Subject performance
#         subject_performance = academic_records.values('subject').annotate(
#             avg_percentage=Avg('percentage'),
#             count=Count('id')
#         ).order_by('-avg_percentage')
#     else:
#         avg_marks = avg_percentage = 0
#         grade_dist = {}
#         subject_performance = []
    
#     # Recent activity
#     week_ago = timezone.now() - timedelta(days=7)
#     recent_records = academic_records.filter(created_at__gte=week_ago).count()
    
#     # Top performers
#     top_performers = academic_records.select_related('soldier__user').order_by('-percentage')[:5]
    
#     # Monthly trends
#     monthly_data = academic_records.filter(
#         created_at__gte=timezone.now() - timedelta(days=30)
#     ).extra({
#         'week': "strftime('%%Y-%%W', created_at)"
#     }).values('week').annotate(
#         avg_percentage=Avg('percentage'),
#         count=Count('id')
#     ).order_by('week')
    
#     return {
#         'total_records': total_records,
#         'avg_marks': round(avg_marks, 1),
#         'avg_percentage': round(avg_percentage, 1),
#         'grade_distribution': dict(grade_dist),
#         'subject_performance': list(subject_performance),
#         'recent_records': recent_records,
#         'top_performers': list(top_performers),
#         'monthly_data': list(monthly_data),
#     }

# def get_soldier_analytics(user):
#     """Soldier dashboard analytics"""
#     from fitness.models import FitnessRecord
#     from academics.models import AcademicRecord
    
#     try:
#         soldier = user.soldier_profile
#     except:
#         return {}
    
#     # Fitness analytics
#     fitness_records = FitnessRecord.objects.filter(soldier=soldier).order_by('-date')
#     total_fitness_records = fitness_records.count()
    
#     if total_fitness_records > 0:
#         latest_fitness = fitness_records.first()
#         fitness_trend = fitness_records.values('date').annotate(
#             pushups=Avg('pushups'),
#             running=Avg('running_distance'),
#             accuracy=Avg('shooting_accuracy')
#         ).order_by('date')[:10]  # Last 10 records
#     else:
#         latest_fitness = None
#         fitness_trend = []
    
#     # Academic analytics
#     academic_records = AcademicRecord.objects.filter(soldier=soldier).order_by('-created_at')
#     total_academic_records = academic_records.count()
    
#     if total_academic_records > 0:
#         latest_academic = academic_records.first()
#         academic_trend = academic_records.values('created_at').annotate(
#             percentage=Avg('percentage')
#         ).order_by('created_at')[:10]
        
#         # Subject-wise performance
#         subject_scores = academic_records.values('subject').annotate(
#             avg_percentage=Avg('percentage'),
#             best_score=Max('percentage')
#         ).order_by('-avg_percentage')
#     else:
#         latest_academic = None
#         academic_trend = []
#         subject_scores = []
    
#     # Overall performance
#     if total_fitness_records > 0 and total_academic_records > 0:
#         fitness_score = (latest_fitness.pushups / 50 * 100) if latest_fitness else 0
#         academic_score = latest_academic.percentage if latest_academic else 0
#         overall_score = (fitness_score + academic_score) / 2
#     else:
#         overall_score = 0
    
#     return {
#         'soldier': soldier,
#         'total_fitness_records': total_fitness_records,
#         'total_academic_records': total_academic_records,
#         'latest_fitness': latest_fitness,
#         'latest_academic': latest_academic,
#         'fitness_trend': list(fitness_trend),
#         'academic_trend': list(academic_trend),
#         'subject_scores': list(subject_scores),
#         'overall_score': round(overall_score, 1),
#     }


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg, Max, Min, Count
from django.utils import timezone
from datetime import timedelta
from users.models import User
from users.forms import UserCreateForm, UserEditForm
from soldiers.models import Soldier
from soldiers.forms import SoldierCreateForm, SoldierEditForm
from fitness.models import FitnessRecord
from fitness.forms import FitnessRecordForm
from academics.models import AcademicRecord
from academics.forms import AcademicRecordForm
from collections import defaultdict

def api_root_view(request):
    return redirect('api-root')

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user
    role = getattr(user, 'role', 'soldier')
    
    # Get analytics data based on user role
    analytics_data = get_dashboard_analytics(request.user)
    
    context = {
        'user': user,
        'role': role,
        'analytics': analytics_data,
    }
    
    template_map = {
        'admin': 'admin/dashboard.html',
        'trainer': 'trainer/dashboard.html', 
        'teacher': 'teacher/dashboard.html',
        'soldier': 'soldier/dashboard.html',
    }
    
    template = template_map.get(role, 'dashboard.html')
    
    return render(request, template, context)

def get_dashboard_analytics(user):
    """Get analytics data for dashboard based on user role"""
    if user.role == 'admin':
        return get_admin_analytics()
    elif user.role == 'trainer':
        return get_trainer_analytics(user)
    elif user.role == 'teacher':
        return get_teacher_analytics(user)
    else:  # soldier
        return get_soldier_analytics(user)

def get_admin_analytics():
    """Admin dashboard analytics"""
    from users.models import User
    from soldiers.models import Soldier
    from fitness.models import FitnessRecord
    from academics.models import AcademicRecord
    
    # User statistics
    total_users = User.objects.count()
    users_by_role = User.objects.values('role').annotate(count=Count('id'))
    
    # Soldier statistics
    total_soldiers = Soldier.objects.count()
    soldiers_by_rank = Soldier.objects.values('rank').annotate(count=Count('id'))
    
    # Fitness statistics
    fitness_records = FitnessRecord.objects.all()
    total_fitness_records = fitness_records.count()
    avg_pushups = fitness_records.aggregate(avg=Avg('pushups'))['avg'] or 0
    avg_running = fitness_records.aggregate(avg=Avg('running_distance'))['avg'] or 0
    
    # Academic statistics
    academic_records = AcademicRecord.objects.all()
    total_academic_records = academic_records.count()
    avg_percentage = academic_records.aggregate(avg=Avg('percentage'))['avg'] or 0
    
    # Recent activity (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_users = User.objects.filter(date_joined__gte=week_ago).count()
    recent_fitness = FitnessRecord.objects.filter(created_at__gte=week_ago).count()
    recent_academics = AcademicRecord.objects.filter(created_at__gte=week_ago).count()
    
    # Performance trends (last 30 days) - FIXED: Using TruncDate instead of extra()
    month_ago = timezone.now() - timedelta(days=30)
    
    # Fitness trend - using date field directly since FitnessRecord has date field
    fitness_trend = FitnessRecord.objects.filter(
        date__gte=month_ago.date()
    ).values('date').annotate(
        count=Count('id'),
        avg_pushups=Avg('pushups'),
        avg_running=Avg('running_distance')
    ).order_by('date')
    
    # Academic trend - using created_at with date lookup
    academic_trend = AcademicRecord.objects.filter(
        created_at__date__gte=month_ago.date()
    ).values('created_at__date').annotate(
        count=Count('id'),
        avg_percentage=Avg('percentage')
    ).order_by('created_at__date')
    
    return {
        'total_users': total_users,
        'users_by_role': list(users_by_role),
        'total_soldiers': total_soldiers,
        'soldiers_by_rank': list(soldiers_by_rank),
        'total_fitness_records': total_fitness_records,
        'avg_pushups': round(avg_pushups, 1),
        'avg_running': round(avg_running, 2),
        'total_academic_records': total_academic_records,
        'avg_percentage': round(avg_percentage, 1),
        'recent_activity': {
            'users': recent_users,
            'fitness': recent_fitness,
            'academics': recent_academics,
        },
        'fitness_trend': list(fitness_trend),
        'academic_trend': list(academic_trend),
    }

def get_trainer_analytics(user):
    """Trainer dashboard analytics"""
    from soldiers.models import Soldier
    from fitness.models import FitnessRecord
    
    # Soldier statistics
    assigned_soldiers = Soldier.objects.filter(assigned_trainer=user)
    total_soldiers = assigned_soldiers.count()
    
    # Fitness statistics for assigned soldiers
    fitness_records = FitnessRecord.objects.filter(soldier__assigned_trainer=user)
    total_records = fitness_records.count()
    
    if total_records > 0:
        avg_pushups = fitness_records.aggregate(avg=Avg('pushups'))['avg'] or 0
        avg_running = fitness_records.aggregate(avg=Avg('running_distance'))['avg'] or 0
        avg_accuracy = fitness_records.aggregate(avg=Avg('shooting_accuracy'))['avg'] or 0
    else:
        avg_pushups = avg_running = avg_accuracy = 0
    
    # Recent records (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_records = fitness_records.filter(created_at__gte=week_ago).count()
    
    # Top performers
    top_performers = assigned_soldiers.annotate(
        avg_pushups=Avg('fitness_records__pushups'),
        avg_running=Avg('fitness_records__running_distance'),
        record_count=Count('fitness_records')
    ).filter(record_count__gt=0).order_by('-avg_pushups')[:5]
    
    # Monthly progress - using date field
    monthly_data = fitness_records.filter(
        date__gte=(timezone.now() - timedelta(days=30)).date()
    ).values('date').annotate(
        avg_pushups=Avg('pushups'),
        avg_running=Avg('running_distance'),
        count=Count('id')
    ).order_by('date')
    
    return {
        'total_soldiers': total_soldiers,
        'total_records': total_records,
        'avg_pushups': round(avg_pushups, 1),
        'avg_running': round(avg_running, 2),
        'avg_accuracy': round(avg_accuracy, 1),
        'recent_records': recent_records,
        'top_performers': list(top_performers),
        'monthly_data': list(monthly_data),
    }

def get_teacher_analytics(user):
    """Teacher dashboard analytics"""
    from academics.models import AcademicRecord
    from soldiers.models import Soldier
    
    # Academic statistics
    academic_records = AcademicRecord.objects.filter(created_by=user)
    total_records = academic_records.count()
    
    if total_records > 0:
        avg_marks = academic_records.aggregate(avg=Avg('marks'))['avg'] or 0
        avg_percentage = academic_records.aggregate(avg=Avg('percentage'))['avg'] or 0
        
        # Subject performance
        subject_performance = academic_records.values('subject').annotate(
            avg_percentage=Avg('percentage'),
            count=Count('id')
        ).order_by('-avg_percentage')
    else:
        avg_marks = avg_percentage = 0
        subject_performance = []
    
    # Recent activity
    week_ago = timezone.now() - timedelta(days=7)
    recent_records = academic_records.filter(created_at__gte=week_ago).count()
    
    # Top performers
    top_performers = academic_records.select_related('soldier__user').order_by('-percentage')[:5]
    
    # Monthly trends - using created_at with date lookup
    monthly_data = academic_records.filter(
        created_at__date__gte=(timezone.now() - timedelta(days=30)).date()
    ).values('created_at__date').annotate(
        avg_percentage=Avg('percentage'),
        count=Count('id')
    ).order_by('created_at__date')
    
    return {
        'total_records': total_records,
        'avg_marks': round(avg_marks, 1),
        'avg_percentage': round(avg_percentage, 1),
        'subject_performance': list(subject_performance),
        'recent_records': recent_records,
        'top_performers': list(top_performers),
        'monthly_data': list(monthly_data),
    }

def get_soldier_analytics(user):
    """Soldier dashboard analytics"""
    from fitness.models import FitnessRecord
    from academics.models import AcademicRecord
    
    try:
        soldier = user.soldier_profile
    except Soldier.DoesNotExist:
        return {}
    
    # Fitness analytics
    fitness_records = FitnessRecord.objects.filter(soldier=soldier).order_by('-date')
    total_fitness_records = fitness_records.count()
    
    if total_fitness_records > 0:
        latest_fitness = fitness_records.first()
        # Get last 10 fitness records for trend
        fitness_trend = fitness_records.values('date', 'pushups', 'running_distance', 'shooting_accuracy')[:10]
    else:
        latest_fitness = None
        fitness_trend = []
    
    # Academic analytics
    academic_records = AcademicRecord.objects.filter(soldier=soldier).order_by('-created_at')
    total_academic_records = academic_records.count()
    
    if total_academic_records > 0:
        latest_academic = academic_records.first()
        # Get last 10 academic records for trend
        academic_trend = academic_records.values('created_at', 'percentage')[:10]
        
        # Subject-wise performance
        subject_scores = academic_records.values('subject').annotate(
            avg_percentage=Avg('percentage'),
            best_score=Max('percentage')
        ).order_by('-avg_percentage')
    else:
        latest_academic = None
        academic_trend = []
        subject_scores = []
    
    # Overall performance
    if total_fitness_records > 0 and total_academic_records > 0:
        fitness_score = (latest_fitness.pushups / 50 * 100) if latest_fitness and latest_fitness.pushups else 0
        academic_score = latest_academic.percentage if latest_academic else 0
        overall_score = (fitness_score + academic_score) / 2
    else:
        overall_score = 0
    
    return {
        'soldier': soldier,
        'total_fitness_records': total_fitness_records,
        'total_academic_records': total_academic_records,
        'latest_fitness': latest_fitness,
        'latest_academic': latest_academic,
        'fitness_trend': list(fitness_trend),
        'academic_trend': list(academic_trend),
        'subject_scores': list(subject_scores),
        'overall_score': round(overall_score, 1),
    }

@login_required
def user_management(request):
    """User management dashboard for admin"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'users': users,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'admins': users.filter(role='admin').count(),
        'trainers': users.filter(role='trainer').count(),
        'teachers': users.filter(role='teacher').count(),
        'soldiers': users.filter(role='soldier').count(),
    }
    
    return render(request, 'admin/user_management.html', context)

@login_required
def create_user(request):
    """Create new user"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('user_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreateForm()
    
    return render(request, 'admin/user_form.html', {
        'form': form,
        'title': 'Create New User',
        'submit_text': 'Create User'
    })

@login_required
def edit_user(request, user_id):
    """Edit existing user"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} updated successfully!')
            return redirect('user_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'admin/user_form.html', {
        'form': form,
        'title': f'Edit User: {user.username}',
        'submit_text': 'Update User',
        'user': user
    })

@login_required
@require_http_methods(["POST"])
def toggle_user_status(request, user_id):
    """Activate/Deactivate user"""
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    user = get_object_or_404(User, id=user_id)
    
    # Prevent self-deactivation
    if user == request.user:
        return JsonResponse({'error': 'Cannot deactivate your own account'}, status=400)
    
    user.is_active = not user.is_active
    user.save()
    
    action = 'activated' if user.is_active else 'deactivated'
    return JsonResponse({
        'success': True,
        'message': f'User {user.username} {action} successfully',
        'is_active': user.is_active
    })

@login_required
@require_http_methods(["POST"])
def delete_user(request, user_id):
    """Delete user"""
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    user = get_object_or_404(User, id=user_id)
    
    # Prevent self-deletion
    if user == request.user:
        return JsonResponse({'error': 'Cannot delete your own account'}, status=400)
    
    username = user.username
    user.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'User {username} deleted successfully'
    })
    
@login_required
def soldier_management(request):
    """Soldier management dashboard for trainers and admins"""
    if request.user.role not in ['admin', 'trainer']:
        messages.error(request, 'Access denied. Trainer or Admin privileges required.')
        return redirect('dashboard')
    
    # Filter soldiers based on user role
    if request.user.role == 'admin':
        soldiers = Soldier.objects.all().select_related('user', 'assigned_trainer')
    else:  # trainer
        soldiers = Soldier.objects.filter(assigned_trainer=request.user).select_related('user', 'assigned_trainer')
    
    # Get search parameters
    search_query = request.GET.get('search', '')
    rank_filter = request.GET.get('rank', '')
    unit_filter = request.GET.get('unit', '')
    
    # Apply filters
    if search_query:
        soldiers = soldiers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(soldier_id__icontains=search_query) |
            Q(unit__icontains=search_query)
        )
    
    if rank_filter:
        soldiers = soldiers.filter(rank=rank_filter)
    
    if unit_filter:
        soldiers = soldiers.filter(unit__icontains=unit_filter)
    
    soldiers = soldiers.order_by('-created_at')
    
    # Get unique ranks and units for filters
    ranks = Soldier.RANK_CHOICES
    units = Soldier.objects.values_list('unit', flat=True).distinct()
    
    context = {
        'soldiers': soldiers,
        'total_soldiers': soldiers.count(),
        'ranks': ranks,
        'units': units,
        'search_query': search_query,
        'rank_filter': rank_filter,
        'unit_filter': unit_filter,
    }
    
    return render(request, 'trainer/soldier_management.html', context)

@login_required
def create_soldier(request):
    """Create new soldier"""
    if request.user.role not in ['admin', 'trainer']:
        messages.error(request, 'Access denied. Trainer or Admin privileges required.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SoldierCreateForm(request.user, request.POST)
        if form.is_valid():
            soldier = form.save()
            messages.success(request, f'Soldier {soldier.user.get_full_name()} created successfully!')
            return redirect('soldier_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SoldierCreateForm(request.user)
    
    return render(request, 'trainer/soldier_form.html', {
        'form': form,
        'title': 'Create New Soldier',
        'submit_text': 'Create Soldier'
    })

@login_required
def edit_soldier(request, soldier_id):
    """Edit existing soldier"""
    if request.user.role not in ['admin', 'trainer']:
        messages.error(request, 'Access denied. Trainer or Admin privileges required.')
        return redirect('dashboard')
    
    soldier = get_object_or_404(Soldier, id=soldier_id)
    
    # Check if trainer is allowed to edit this soldier
    if request.user.role == 'trainer' and soldier.assigned_trainer != request.user:
        messages.error(request, 'Access denied. You can only edit soldiers assigned to you.')
        return redirect('soldier_management')
    
    if request.method == 'POST':
        form = SoldierEditForm(request.user, request.POST, instance=soldier)
        if form.is_valid():
            soldier = form.save()
            messages.success(request, f'Soldier {soldier.user.get_full_name()} updated successfully!')
            return redirect('soldier_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SoldierEditForm(request.user, instance=soldier)
    
    return render(request, 'trainer/soldier_form.html', {
        'form': form,
        'title': f'Edit Soldier: {soldier.user.get_full_name()}',
        'submit_text': 'Update Soldier',
        'soldier': soldier
    })

@login_required
def soldier_detail(request, soldier_id):
    """View soldier details"""
    if request.user.role not in ['admin', 'trainer']:
        messages.error(request, 'Access denied. Trainer or Admin privileges required.')
        return redirect('dashboard')
    
    soldier = get_object_or_404(Soldier, id=soldier_id)
    
    # Check if trainer is allowed to view this soldier
    if request.user.role == 'trainer' and soldier.assigned_trainer != request.user:
        messages.error(request, 'Access denied. You can only view soldiers assigned to you.')
        return redirect('soldier_management')
    
    # Get fitness and academic records
    fitness_records = FitnessRecord.objects.filter(soldier=soldier).order_by('-date')[:5]
    academic_records = AcademicRecord.objects.filter(soldier=soldier).order_by('-created_at')[:5]
    
    # Calculate service duration
    from datetime import date
    today = date.today()
    joining_date = soldier.joining_date
    
    years = today.year - joining_date.year
    months = today.month - joining_date.month
    
    if today.day < joining_date.day:
        months -= 1
    
    if months < 0:
        years -= 1
        months += 12
    
    service_duration = f"{years} year{'s' if years != 1 else ''}"
    if months > 0:
        service_duration += f" {months} month{'s' if months != 1 else ''}"
    
    context = {
        'soldier': soldier,
        'fitness_records': fitness_records,
        'academic_records': academic_records,
        'service_duration': service_duration,
    }
    
    return render(request, 'trainer/soldier_detail.html', context)

@login_required
@require_http_methods(["POST"])
def delete_soldier(request, soldier_id):
    """Delete soldier"""
    if request.user.role not in ['admin', 'trainer']:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    soldier = get_object_or_404(Soldier, id=soldier_id)
    
    # Check if trainer is allowed to delete this soldier
    if request.user.role == 'trainer' and soldier.assigned_trainer != request.user:
        return JsonResponse({'error': 'Access denied. You can only delete soldiers assigned to you.'}, status=403)
    
    soldier_name = soldier.user.get_full_name()
    soldier_id_str = soldier.soldier_id
    
    # Delete the soldier (this will not delete the user)
    soldier.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'Soldier {soldier_name} ({soldier_id_str}) deleted successfully'
    })
    
@login_required
def fitness_records(request):
    """Fitness records management for trainers and admins"""
    if request.user.role not in ['admin', 'trainer']:
        messages.error(request, 'Access denied. Trainer or Admin privileges required.')
        return redirect('dashboard')
    
    # Filter records based on user role
    if request.user.role == 'admin':
        records = FitnessRecord.objects.all().select_related('soldier__user', 'created_by')
    else:  # trainer
        records = FitnessRecord.objects.filter(
            Q(soldier__assigned_trainer=request.user) | Q(created_by=request.user)
        ).select_related('soldier__user', 'created_by')
    
    # Get filter parameters
    soldier_filter = request.GET.get('soldier', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Apply filters
    if soldier_filter:
        records = records.filter(soldier_id=soldier_filter)
    
    if date_from:
        records = records.filter(date__gte=date_from)
    
    if date_to:
        records = records.filter(date__lte=date_to)
    
    records = records.order_by('-date', '-created_at')
    
    # Get soldiers for filter dropdown
    if request.user.role == 'admin':
        soldiers = Soldier.objects.all().select_related('user')
    else:
        soldiers = Soldier.objects.filter(assigned_trainer=request.user).select_related('user')
    
    # Calculate some statistics
    total_records = records.count()
    if total_records > 0:
        avg_pushups = records.aggregate(Avg('pushups'))['pushups__avg'] or 0
        avg_running = records.aggregate(Avg('running_distance'))['running_distance__avg'] or 0
        avg_accuracy = records.aggregate(Avg('shooting_accuracy'))['shooting_accuracy__avg'] or 0
    else:
        avg_pushups = avg_running = avg_accuracy = 0
    
    context = {
        'records': records,
        'soldiers': soldiers,
        'total_records': total_records,
        'avg_pushups': round(avg_pushups, 1),
        'avg_running': round(avg_running, 2),
        'avg_accuracy': round(avg_accuracy, 1),
        'soldier_filter': soldier_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'trainer/fitness_records.html', context)

@login_required
def create_fitness_record(request):
    """Create new fitness record"""
    if request.user.role not in ['admin', 'trainer']:
        messages.error(request, 'Access denied. Trainer or Admin privileges required.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = FitnessRecordForm(request.user, request.POST)
        if form.is_valid():
            fitness_record = form.save(commit=False)
            fitness_record.created_by = request.user
            fitness_record.save()
            
            messages.success(request, f'Fitness record for {fitness_record.soldier.user.get_full_name()} created successfully!')
            return redirect('fitness_records')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FitnessRecordForm(request.user)
    
    return render(request, 'trainer/fitness_form.html', {
        'form': form,
        'title': 'Create Fitness Record',
        'submit_text': 'Create Record'
    })

@login_required
def edit_fitness_record(request, record_id):
    """Edit existing fitness record"""
    if request.user.role not in ['admin', 'trainer']:
        messages.error(request, 'Access denied. Trainer or Admin privileges required.')
        return redirect('dashboard')
    
    record = get_object_or_404(FitnessRecord, id=record_id)
    
    # Check permissions
    if request.user.role == 'trainer' and record.soldier.assigned_trainer != request.user and record.created_by != request.user:
        messages.error(request, 'Access denied. You can only edit records for your assigned soldiers.')
        return redirect('fitness_records')
    
    if request.method == 'POST':
        form = FitnessRecordForm(request.user, request.POST, instance=record)
        if form.is_valid():
            fitness_record = form.save()
            messages.success(request, f'Fitness record for {fitness_record.soldier.user.get_full_name()} updated successfully!')
            return redirect('fitness_records')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FitnessRecordForm(request.user, instance=record)
    
    return render(request, 'trainer/fitness_form.html', {
        'form': form,
        'title': f'Edit Fitness Record - {record.soldier.user.get_full_name()}',
        'submit_text': 'Update Record',
        'record': record
    })

@login_required
def fitness_record_detail(request, record_id):
    """View fitness record details"""
    if request.user.role not in ['admin', 'trainer']:
        messages.error(request, 'Access denied. Trainer or Admin privileges required.')
        return redirect('dashboard')
    
    record = get_object_or_404(FitnessRecord, id=record_id)
    
    # Check permissions
    if request.user.role == 'trainer' and record.soldier.assigned_trainer != request.user and record.created_by != request.user:
        messages.error(request, 'Access denied. You can only view records for your assigned soldiers.')
        return redirect('fitness_records')
    
    # Get performance evaluation
    performance = record.evaluate_performance()
    
    context = {
        'record': record,
        'performance': performance,
    }
    
    return render(request, 'trainer/fitness_detail.html', context)

@login_required
@require_http_methods(["POST"])
def delete_fitness_record(request, record_id):
    """Delete fitness record"""
    if request.user.role not in ['admin', 'trainer']:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    record = get_object_or_404(FitnessRecord, id=record_id)
    
    # Check permissions
    if request.user.role == 'trainer' and record.soldier.assigned_trainer != request.user and record.created_by != request.user:
        return JsonResponse({'error': 'Access denied. You can only delete records for your assigned soldiers.'}, status=403)
    
    soldier_name = record.soldier.user.get_full_name()
    record_date = record.date
    
    record.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'Fitness record for {soldier_name} on {record_date} deleted successfully'
    })

@login_required
def soldier_fitness_history(request, soldier_id):
    """View fitness history for a specific soldier"""
    if request.user.role not in ['admin', 'trainer']:
        messages.error(request, 'Access denied. Trainer or Admin privileges required.')
        return redirect('dashboard')
    
    soldier = get_object_or_404(Soldier, id=soldier_id)
    
    # Check permissions
    if request.user.role == 'trainer' and soldier.assigned_trainer != request.user:
        messages.error(request, 'Access denied. You can only view fitness history for your assigned soldiers.')
        return redirect('fitness_records')
    
    records = FitnessRecord.objects.filter(soldier=soldier).order_by('-date')
    
    # Calculate statistics
    if records.exists():
        stats = records.aggregate(
            avg_pushups=Avg('pushups'),
            avg_running_distance=Avg('running_distance'),
            avg_running_time=Avg('running_time'),
            avg_bmi=Avg('bmi'),
            avg_shooting_accuracy=Avg('shooting_accuracy'),
            max_pushups=Max('pushups'),
            max_running_distance=Max('running_distance'),
            min_running_time=Min('running_time'),
            max_shooting_accuracy=Max('shooting_accuracy'),
        )
        
        # Calculate progress (latest vs oldest record)
        latest_record = records.first()
        oldest_record = records.last()
        
        progress = {
            'pushups': latest_record.pushups - oldest_record.pushups,
            'running_distance': latest_record.running_distance - oldest_record.running_distance,
            'running_time': oldest_record.running_time - latest_record.running_time,  # Lower time is better
            'shooting_accuracy': latest_record.shooting_accuracy - oldest_record.shooting_accuracy,
        }
    else:
        stats = {}
        progress = {}
    
    context = {
        'soldier': soldier,
        'records': records,
        'stats': stats,
        'progress': progress,
        'total_records': records.count(),
    }
    
    return render(request, 'trainer/soldier_fitness_history.html', context)

@login_required
def academic_records(request):
    """Academic records management for teachers and admins"""
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, 'Access denied. Teacher or Admin privileges required.')
        return redirect('dashboard')
    
    # Filter records based on user role
    if request.user.role == 'admin':
        records = AcademicRecord.objects.all().select_related('soldier__user', 'created_by')
    else:  # teacher
        records = AcademicRecord.objects.filter(created_by=request.user).select_related('soldier__user', 'created_by')
    
    # Get filter parameters
    soldier_filter = request.GET.get('soldier', '')
    subject_filter = request.GET.get('subject', '')
    exam_filter = request.GET.get('exam', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Apply filters
    if soldier_filter:
        records = records.filter(soldier_id=soldier_filter)
    
    if subject_filter:
        records = records.filter(subject=subject_filter)
    
    if exam_filter:
        records = records.filter(exam_name__icontains=exam_filter)
    
    if date_from:
        records = records.filter(created_at__date__gte=date_from)
    
    if date_to:
        records = records.filter(created_at__date__lte=date_to)
    
    records = records.order_by('-created_at')
    
    # Get soldiers and subjects for filter dropdowns
    if request.user.role == 'admin':
        soldiers = Soldier.objects.all().select_related('user')
    else:
        # Teachers can see all soldiers for academic records
        soldiers = Soldier.objects.all().select_related('user')
    
    subjects = AcademicRecord.SUBJECT_CHOICES
    exam_names = AcademicRecord.objects.values_list('exam_name', flat=True).distinct()
    
    # Calculate statistics
    total_records = records.count()
    if total_records > 0:
        avg_marks = records.aggregate(Avg('marks'))['marks__avg'] or 0
        avg_percentage = records.aggregate(Avg('percentage'))['percentage__avg'] or 0
        top_performer = records.order_by('-percentage').first()
    else:
        avg_marks = avg_percentage = 0
        top_performer = None
    
    context = {
        'records': records,
        'soldiers': soldiers,
        'subjects': subjects,
        'exam_names': exam_names,
        'total_records': total_records,
        'avg_marks': round(avg_marks, 1),
        'avg_percentage': round(avg_percentage, 1),
        'top_performer': top_performer,
        'soldier_filter': soldier_filter,
        'subject_filter': subject_filter,
        'exam_filter': exam_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'teacher/academic_records.html', context)

@login_required
def create_academic_record(request):
    """Create new academic record"""
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, 'Access denied. Teacher or Admin privileges required.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AcademicRecordForm(request.user, request.POST)
        if form.is_valid():
            academic_record = form.save(commit=False)
            academic_record.created_by = request.user
            academic_record.save()
            
            messages.success(request, f'Academic record for {academic_record.soldier.user.get_full_name()} created successfully!')
            return redirect('academic_records')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AcademicRecordForm(request.user)
    
    return render(request, 'teacher/academic_form.html', {
        'form': form,
        'title': 'Create Academic Record',
        'submit_text': 'Create Record'
    })

@login_required
def edit_academic_record(request, record_id):
    """Edit existing academic record"""
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, 'Access denied. Teacher or Admin privileges required.')
        return redirect('dashboard')
    
    record = get_object_or_404(AcademicRecord, id=record_id)
    
    # Check permissions
    if request.user.role == 'teacher' and record.created_by != request.user:
        messages.error(request, 'Access denied. You can only edit records created by you.')
        return redirect('academic_records')
    
    if request.method == 'POST':
        form = AcademicRecordForm(request.user, request.POST, instance=record)
        if form.is_valid():
            academic_record = form.save()
            messages.success(request, f'Academic record for {academic_record.soldier.user.get_full_name()} updated successfully!')
            return redirect('academic_records')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AcademicRecordForm(request.user, instance=record)
    
    return render(request, 'teacher/academic_form.html', {
        'form': form,
        'title': f'Edit Academic Record - {record.soldier.user.get_full_name()}',
        'submit_text': 'Update Record',
        'record': record
    })

@login_required
def academic_record_detail(request, record_id):
    """View academic record details"""
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, 'Access denied. Teacher or Admin privileges required.')
        return redirect('dashboard')
    
    record = get_object_or_404(AcademicRecord, id=record_id)
    
    # Check permissions
    if request.user.role == 'teacher' and record.created_by != request.user:
        messages.error(request, 'Access denied. You can only view records created by you.')
        return redirect('academic_records')
    
    # Get performance evaluation
    performance = record.evaluate_performance()
    
    context = {
        'record': record,
        'performance': performance,
    }
    
    return render(request, 'teacher/academic_detail.html', context)

@login_required
@require_http_methods(["POST"])
def delete_academic_record(request, record_id):
    """Delete academic record"""
    if request.user.role not in ['admin', 'teacher']:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    record = get_object_or_404(AcademicRecord, id=record_id)
    
    # Check permissions
    if request.user.role == 'teacher' and record.created_by != request.user:
        return JsonResponse({'error': 'Access denied. You can only delete records created by you.'}, status=403)
    
    soldier_name = record.soldier.user.get_full_name()
    exam_name = record.exam_name
    
    record.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'Academic record for {soldier_name} ({exam_name}) deleted successfully'
    })

@login_required
def soldier_academic_history(request, soldier_id):
    """View academic history for a specific soldier"""
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, 'Access denied. Teacher or Admin privileges required.')
        return redirect('dashboard')
    
    soldier = get_object_or_404(Soldier, id=soldier_id)
    
    records = AcademicRecord.objects.filter(soldier=soldier).order_by('-created_at')
    
    # Calculate statistics
    if records.exists():
        stats = records.aggregate(
            avg_marks=Avg('marks'),
            avg_percentage=Avg('percentage'),
            max_marks=Max('marks'),
            max_percentage=Max('percentage'),
            total_exams=Count('id'),
            distinct_subjects=Count('subject', distinct=True)
        )
        
        # Subject-wise performance
        subject_stats = records.values('subject').annotate(
            avg_marks=Avg('marks'),
            avg_percentage=Avg('percentage'),
            count=Count('id')
        ).order_by('-avg_percentage')
        
        # Progress (latest vs average)
        latest_record = records.first()
        overall_avg = stats['avg_percentage'] or 0
        progress = latest_record.percentage - overall_avg if latest_record else 0
    else:
        stats = {}
        subject_stats = []
        progress = 0
    
    context = {
        'soldier': soldier,
        'records': records,
        'stats': stats,
        'subject_stats': subject_stats,
        'progress': progress,
        'total_records': records.count(),
    }
    
    return render(request, 'teacher/soldier_academic_history.html', context)

@login_required
def subject_analytics(request):
    """View analytics by subject"""
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, 'Access denied. Teacher or Admin privileges required.')
        return redirect('dashboard')
    
    # Filter records based on user role
    if request.user.role == 'admin':
        records = AcademicRecord.objects.all()
    else:  # teacher
        records = AcademicRecord.objects.filter(created_by=request.user)
    
    # Subject-wise analytics
    subject_analytics = records.values('subject').annotate(
        total_students=Count('soldier', distinct=True),
        total_exams=Count('id'),
        avg_marks=Avg('marks'),
        avg_percentage=Avg('percentage'),
        max_percentage=Max('percentage'),
        min_percentage=Min('percentage')
    ).order_by('-avg_percentage')
    
    # Overall statistics
    total_students = Soldier.objects.count()
    total_records = records.count()
    overall_avg_percentage = records.aggregate(Avg('percentage'))['percentage__avg'] or 0
    
    context = {
        'subject_analytics': subject_analytics,
        'total_students': total_students,
        'total_records': total_records,
        'overall_avg_percentage': round(overall_avg_percentage, 1),
    }
    
    return render(request, 'teacher/subject_analytics.html', context)