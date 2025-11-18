from django.urls import path
from . import views

urlpatterns = [
    path('academics/', views.AcademicRecordListCreateView.as_view(), name='academic-list-create'),
    path('academics/<int:pk>/', views.AcademicRecordDetailView.as_view(), name='academic-detail'),
]