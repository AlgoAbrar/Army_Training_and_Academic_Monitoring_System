from django.urls import path
from . import views

urlpatterns = [
    path('soldiers/', views.SoldierListCreateView.as_view(), name='soldier-list-create'),
    path('soldiers/<int:pk>/', views.SoldierDetailView.as_view(), name='soldier-detail'),
]