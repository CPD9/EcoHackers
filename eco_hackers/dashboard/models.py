from django.db import models

class EnergyValveData(models.Model):
    device_id = models.CharField(max_length=50)
    sample_time = models.DateTimeField(null=True, blank=True)
    t1_remote_k = models.FloatField(null=True, blank=True)
    t2_embeded_k = models.FloatField(null=True, blank=True)
    delta_t_k = models.FloatField(null=True, blank=True)
    flow_volume_total_m3 = models.FloatField(null=True, blank=True)
    operating_hours = models.FloatField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['device_id']),
            models.Index(fields=['sample_time']),
        ]
        
    def __str__(self):
        return f"{self.device_id} - {self.sample_time}"