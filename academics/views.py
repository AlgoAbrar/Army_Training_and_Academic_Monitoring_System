from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api.permissions import IsTeacherOrAdmin
from .models import AcademicRecord
from .serializers import AcademicRecordSerializer, AcademicRecordCreateSerializer

class AcademicRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacherOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['soldier', 'exam_name', 'subject']
    search_fields = ['soldier__user__first_name', 'soldier__user__last_name', 'soldier__soldier_id', 'exam_name']
    ordering_fields = ['marks', 'created_at']
    
    def get_queryset(self):
        soldier_id = self.kwargs.get('soldier_pk')
        
        if soldier_id:
            # For nested routes: /soldiers/{id}/academic-records/
            queryset = AcademicRecord.objects.filter(soldier_id=soldier_id)
        else:
            # For main route: /academics/
            queryset = AcademicRecord.objects.all()
        
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AcademicRecordCreateSerializer
        return AcademicRecordSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        subject = request.query_params.get('subject', '')
        if subject:
            records = self.get_queryset().filter(subject=subject)
            serializer = self.get_serializer(records, many=True)
            return Response(serializer.data)
        return Response([])