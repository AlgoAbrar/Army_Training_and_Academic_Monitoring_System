from rest_framework import serializers
from .models import FitnessRecord

class FitnessRecordSerializer(serializers.ModelSerializer):
    soldier_name = serializers.CharField(source='soldier.user.get_full_name', read_only=True)
    soldier_id = serializers.CharField(source='soldier.soldier_id', read_only=True)

    class Meta:
        model = FitnessRecord
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')

class FitnessRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessRecord
        fields = '__all__'
        read_only_fields = ('created_by',)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)