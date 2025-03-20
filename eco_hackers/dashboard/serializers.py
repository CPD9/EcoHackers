from rest_framework import serializers
from .models import EnergyValveData

class EnergyValveDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyValveData
        fields = '__all__'