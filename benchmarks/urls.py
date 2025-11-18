from django.urls import path
from . import views

urlpatterns = [
    path('benchmarks/', views.BenchmarkListCreateView.as_view(), name='benchmark-list-create'),
    path('benchmarks/<int:pk>/', views.BenchmarkDetailView.as_view(), name='benchmark-detail'),
]