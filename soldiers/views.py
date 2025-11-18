from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api.permissions import IsTrainerOrAdmin
from .models import Soldier
from .serializers import SoldierSerializer, SoldierCreateSerializer

class SoldierViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTrainerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rank', 'unit']
    search_fields = ['user__first_name', 'user__last_name', 'soldier_id', 'unit']
    ordering_fields = ['rank', 'joining_date', 'created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Soldier.objects.all()
        elif user.role == 'trainer':
            return Soldier.objects.filter(assigned_trainer=user)
        return Soldier.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return SoldierCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SoldierCreateSerializer
        return SoldierSerializer
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def fitness_summary(self, request, pk=None):
        soldier = self.get_object()
        # Add fitness summary logic here
        return Response({'fitness_summary': 'To be implemented'})
    
    @action(detail=True, methods=['get'])
    def academic_summary(self, request, pk=None):
        soldier = self.get_object()
        # Add academic summary logic here
        return Response({'academic_summary': 'To be implemented'})