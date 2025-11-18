from django.db import models

class Benchmark(models.Model):
    CATEGORY_CHOICES = (
        ('fitness', 'Fitness'),
        ('academic', 'Academic'),
    )
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    metric_name = models.CharField(max_length=50)
    min_value = models.FloatField()
    max_value = models.FloatField(null=True, blank=True)
    label = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['category', 'metric_name']
        ordering = ['category', 'metric_name']

    def __str__(self):
        return f"{self.category} - {self.metric_name} ({self.label})"