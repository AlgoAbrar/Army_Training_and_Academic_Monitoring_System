from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.permissions import IsAdmin
from .models import Benchmark
from .serializers import BenchmarkSerializer

class BenchmarkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = Benchmark.objects.all()
    serializer_class = BenchmarkSerializer
    
    @action(detail=False, methods=['get'])
    def fitness_benchmarks(self, request):
        fitness_benchmarks = Benchmark.objects.filter(category='fitness')
        serializer = self.get_serializer(fitness_benchmarks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def academic_benchmarks(self, request):
        academic_benchmarks = Benchmark.objects.filter(category='academic')
        serializer = self.get_serializer(academic_benchmarks, many=True)
        return Response(serializer.data)