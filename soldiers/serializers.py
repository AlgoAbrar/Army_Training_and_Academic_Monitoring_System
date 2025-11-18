from rest_framework import serializers
from .models import Soldier
from users.serializers import UserSerializer

class SoldierSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    trainer_name = serializers.CharField(source='assigned_trainer.get_full_name', read_only=True)

    class Meta:
        model = Soldier
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class SoldierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soldier
        fields = '__all__'

    def validate_assigned_trainer(self, value):
        if value and value.role != 'trainer':
            raise serializers.ValidationError("Assigned trainer must have trainer role.")
        return value