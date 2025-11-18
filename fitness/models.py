from django.db import models
from soldiers.models import Soldier
from benchmarks.models import Benchmark

# class FitnessRecord(models.Model):
#     soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE, related_name='fitness_records')
#     date = models.DateField()
#     pushups = models.IntegerField(help_text="Number of pushups in 2 minutes")
#     running_distance = models.FloatField(help_text="Distance in kilometers")
#     running_time = models.FloatField(help_text="Time in minutes")
#     bmi = models.FloatField(help_text="Body Mass Index")
#     shooting_accuracy = models.FloatField(help_text="Percentage accuracy")
#     remarks = models.TextField(blank=True, null=True)
#     created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ['soldier', 'date']
#         ordering = ['-date', 'soldier']

#     def __str__(self):
#         return f"{self.soldier} - {self.date}"

class FitnessRecord(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE, related_name='fitness_records')
    date = models.DateField()
    pushups = models.IntegerField(help_text="Number of pushups in 2 minutes")
    running_distance = models.FloatField(help_text="Distance in kilometers")
    running_time = models.FloatField(help_text="Time in minutes")
    bmi = models.FloatField(help_text="Body Mass Index")
    shooting_accuracy = models.FloatField(help_text="Percentage accuracy")
    remarks = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['soldier', 'date']
        ordering = ['-date', 'soldier']

    def __str__(self):
        return f"{self.soldier} - {self.date}"

    def evaluate_performance(self):
        """Evaluate performance based on benchmarks"""
        try:
            # Get benchmarks (you can customize these values)
            benchmarks = {
                'pushups': 40,  # Excellent if >= 40
                'running_distance': 5.0,  # Excellent if >= 5.0 km
                'running_time': 25.0,  # Excellent if <= 25 minutes for 5km
                'shooting_accuracy': 85.0,  # Excellent if >= 85%
                'bmi_min': 18.5,
                'bmi_max': 24.9,
            }
            
            score = 0
            evaluation = {}
            
            # Pushups evaluation
            if self.pushups >= benchmarks['pushups']:
                score += 1
                evaluation['pushups'] = 'Excellent'
            elif self.pushups >= 30:
                evaluation['pushups'] = 'Good'
            elif self.pushups >= 20:
                evaluation['pushups'] = 'Average'
            else:
                evaluation['pushups'] = 'Needs Improvement'
            
            # Running distance evaluation
            if self.running_distance >= benchmarks['running_distance']:
                score += 1
                evaluation['running_distance'] = 'Excellent'
            elif self.running_distance >= 4.0:
                evaluation['running_distance'] = 'Good'
            elif self.running_distance >= 3.0:
                evaluation['running_distance'] = 'Average'
            else:
                evaluation['running_distance'] = 'Needs Improvement'
            
            # Running time evaluation (lower is better)
            if self.running_time <= benchmarks['running_time']:
                score += 1
                evaluation['running_time'] = 'Excellent'
            elif self.running_time <= 30.0:
                evaluation['running_time'] = 'Good'
            elif self.running_time <= 35.0:
                evaluation['running_time'] = 'Average'
            else:
                evaluation['running_time'] = 'Needs Improvement'
            
            # Shooting accuracy evaluation
            if self.shooting_accuracy >= benchmarks['shooting_accuracy']:
                score += 1
                evaluation['shooting_accuracy'] = 'Excellent'
            elif self.shooting_accuracy >= 75.0:
                evaluation['shooting_accuracy'] = 'Good'
            elif self.shooting_accuracy >= 60.0:
                evaluation['shooting_accuracy'] = 'Average'
            else:
                evaluation['shooting_accuracy'] = 'Needs Improvement'
            
            # BMI evaluation
            if benchmarks['bmi_min'] <= self.bmi <= benchmarks['bmi_max']:
                score += 1
                evaluation['bmi'] = 'Healthy'
            elif self.bmi < benchmarks['bmi_min']:
                evaluation['bmi'] = 'Underweight'
            else:
                evaluation['bmi'] = 'Overweight'
            
            # Overall evaluation
            if score >= 4:
                evaluation['overall'] = 'Excellent'
            elif score >= 3:
                evaluation['overall'] = 'Good'
            elif score >= 2:
                evaluation['overall'] = 'Average'
            else:
                evaluation['overall'] = 'Needs Improvement'
            
            return evaluation
            
        except Exception as e:
            return {'overall': 'Evaluation Error'}

    @property
    def performance_color(self):
        """Get color for performance badge"""
        evaluation = self.evaluate_performance()
        overall = evaluation.get('overall', 'Unknown')
        
        color_map = {
            'Excellent': 'bg-green-600',
            'Good': 'bg-blue-600', 
            'Average': 'bg-yellow-600',
            'Needs Improvement': 'bg-red-600',
            'Healthy': 'bg-green-600',
            'Underweight': 'bg-yellow-600',
            'Overweight': 'bg-orange-600',
            'Unknown': 'bg-gray-600'
        }
        
        return color_map.get(overall, 'bg-gray-600')