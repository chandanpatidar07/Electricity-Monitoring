from django.db import models
from django.contrib.auth.models import User

class ApplianceUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appliance_usages')
    appliance_name = models.CharField(max_length=100)
    usage_time_hours = models.FloatField()
    electricity_needed_kwh = models.FloatField()
    electricity_wasted_kwh = models.FloatField()
    cost_per_kwh = models.FloatField()

    @property
    def total_cost(self):
        return (self.electricity_needed_kwh + self.electricity_wasted_kwh) * self.cost_per_kwh

    def __str__(self):
        return f"{self.appliance_name} ({self.user.username})"
