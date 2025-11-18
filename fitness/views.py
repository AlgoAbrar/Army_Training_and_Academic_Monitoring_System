from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api.permissions import IsTrainerOrAdmin
from .models import FitnessRecord
from .serializers import FitnessRecordSerializer, FitnessRecordCreateSerializer

class FitnessRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTrainerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['soldier', 'date']
    search_fields = ['soldier__user__first_name', 'soldier__user__last_name', 'soldier__soldier_id']
    ordering_fields = ['date', 'pushups', 'running_distance']
    
    def get_queryset(self):
        user = self.request.user
        soldier_id = self.kwargs.get('soldier_pk')
        
        if soldier_id:
            # For nested routes: /soldiers/{id}/fitness-records/
            queryset = FitnessRecord.objects.filter(soldier_id=soldier_id)
        else:
            # For main route: /fitness/
            if user.role == 'admin':
                queryset = FitnessRecord.objects.all()
            elif user.role == 'trainer':
                queryset = FitnessRecord.objects.filter(soldier__assigned_trainer=user)
            else:
                queryset = FitnessRecord.objects.none()
        
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FitnessRecordCreateSerializer
        return FitnessRecordSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_records = self.get_queryset().order_by('-date')[:10]
        serializer = self.get_serializer(recent_records, many=True)
        return Response(serializer.data)