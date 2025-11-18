from rest_framework import serializers

class DashboardStatsSerializer(serializers.Serializer):
    total_soldiers = serializers.IntegerField()
    total_trainers = serializers.IntegerField()
    total_teachers = serializers.IntegerField()
    fitness_records_count = serializers.IntegerField()
    academic_records_count = serializers.IntegerField()
    average_fitness_score = serializers.FloatField()
    average_academic_score = serializers.FloatField()