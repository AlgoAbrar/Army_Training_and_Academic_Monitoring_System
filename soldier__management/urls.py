from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from .views import api_root_view, home, login_view, logout_view, dashboard
from .views import user_management, create_user, edit_user, toggle_user_status, delete_user
from .views import soldier_management, create_soldier, edit_soldier, soldier_detail, delete_soldier
from .views import fitness_records, create_fitness_record, edit_fitness_record, fitness_record_detail, delete_fitness_record, soldier_fitness_history
from .views import academic_records, create_academic_record, edit_academic_record, academic_record_detail, delete_academic_record, soldier_academic_history, subject_analytics
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ATAMS - Army Training & Academic Monitoring System API",
        default_version='v1',
        description="API Documentation for Army Training & Academic Monitoring System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@atams.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # User Management URLs
    path('admin/users/', user_management, name='user_management'),
    path('admin/users/create/', create_user, name='create_user'),
    path('admin/users/<int:user_id>/edit/', edit_user, name='edit_user'),
    path('admin/users/<int:user_id>/toggle-status/', toggle_user_status, name='toggle_user_status'),
    path('admin/users/<int:user_id>/delete/', delete_user, name='delete_user'),
    
    # Soldier Management URLs
    path('trainer/soldiers/', soldier_management, name='soldier_management'),
    path('trainer/soldiers/create/', create_soldier, name='create_soldier'),
    path('trainer/soldiers/<int:soldier_id>/edit/', edit_soldier, name='edit_soldier'),
    path('trainer/soldiers/<int:soldier_id>/', soldier_detail, name='soldier_detail'),
    path('trainer/soldiers/<int:soldier_id>/delete/', delete_soldier, name='delete_soldier'),
    
    # Fitness Records URLs
    path('trainer/fitness/', fitness_records, name='fitness_records'),
    path('trainer/fitness/create/', create_fitness_record, name='create_fitness_record'),
    path('trainer/fitness/<int:record_id>/edit/', edit_fitness_record, name='edit_fitness_record'),
    path('trainer/fitness/<int:record_id>/', fitness_record_detail, name='fitness_record_detail'),
    path('trainer/fitness/<int:record_id>/delete/', delete_fitness_record, name='delete_fitness_record'),
    path('trainer/soldiers/<int:soldier_id>/fitness-history/', soldier_fitness_history, name='soldier_fitness_history'),
    
    # Academic Records URLs
    path('teacher/academics/', academic_records, name='academic_records'),
    path('teacher/academics/create/', create_academic_record, name='create_academic_record'),
    path('teacher/academics/<int:record_id>/edit/', edit_academic_record, name='edit_academic_record'),
    path('teacher/academics/<int:record_id>/', academic_record_detail, name='academic_record_detail'),
    path('teacher/academics/<int:record_id>/delete/', delete_academic_record, name='delete_academic_record'),
    path('teacher/soldiers/<int:soldier_id>/academic-history/', soldier_academic_history, name='soldier_academic_history'),
    path('teacher/analytics/subjects/', subject_analytics, name='subject_analytics'),
    
    # API URLs
    path('api/v1/', include('api.urls'), name='api-root'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)