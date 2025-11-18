from rest_framework import serializers
from .models import Benchmark

class BenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benchmark
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')