from django.urls import path
from . import views

urlpatterns = [
    path('fitness/', views.FitnessRecordListCreateView.as_view(), name='fitness-list-create'),
    path('fitness/<int:pk>/', views.FitnessRecordDetailView.as_view(), name='fitness-detail'),
]