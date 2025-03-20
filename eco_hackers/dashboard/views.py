import pandas as pd
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count, Max, Min
from django.db.models.functions import ExtractHour, ExtractWeekDay
from .models import EnergyValveData
from .serializers import EnergyValveDataSerializer

class EnergyValveDataAPIView(APIView):
    def get(self, request):
        queryset = EnergyValveData.objects.all()
        serializer = EnergyValveDataSerializer(queryset, many=True)
        return Response(serializer.data)

class HourlyHeatmapAPIView(APIView):
    def get(self, request):
        # Annotate data with hour and weekday
        data = (
            EnergyValveData.objects
            .annotate(hour=ExtractHour('sample_time'))
            .annotate(weekday=ExtractWeekDay('sample_time'))
            .values('hour', 'weekday')
            .annotate(
                avg_value=Avg('t1_remote_k'),
                count=Count('id')
            )
            .order_by('weekday', 'hour')
        )
        
        # Transform into format needed for heatmap
        result = {
            'hours': sorted(set(item['hour'] for item in data)),
            'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'values': [],
            'counts': []
        }
        
        # Fill in values by day and hour
        for day_idx in range(7):
            day_values = []
            day_counts = []
            for hour in result['hours']:
                # Find matching data point or use defaults
                found = False
                for item in data:
                    if item['weekday'] == day_idx and item['hour'] == hour:
                        day_values.append(item['avg_value'])
                        day_counts.append(item['count'])
                        found = True
                        break
                if not found:
                    day_values.append(None)
                    day_counts.append(0)
            
            result['values'].append(day_values)
            result['counts'].append(day_counts)
            
        return Response(result)

# Add similar views for other visualization types...