from django.db import models
from soldiers.models import Soldier

class AcademicRecord(models.Model):
    SUBJECT_CHOICES = (
        ('military_tactics', 'Military Tactics'),
        ('weapon_training', 'Weapon Training'),
        ('communication', 'Communication'),
        ('leadership', 'Leadership'),
        ('first_aid', 'First Aid'),
        ('physical_training', 'Physical Training'),
        ('general_knowledge', 'General Knowledge'),
    )
    
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE, related_name='academic_records')
    exam_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    marks = models.FloatField()
    total_marks = models.FloatField(default=100)
    percentage = models.FloatField(editable=False)  # Auto-calculated
    remarks = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'soldier']

    def __str__(self):
        return f"{self.soldier} - {self.exam_name} - {self.subject}"

    def save(self, *args, **kwargs):
        # Calculate percentage before saving
        if self.marks and self.total_marks:
            self.percentage = (self.marks / self.total_marks) * 100
        super().save(*args, **kwargs)

    def evaluate_performance(self):
        """Evaluate academic performance based on percentage"""
        percentage = self.percentage
        
        if percentage >= 85:
            return {
                'grade': 'A+',
                'rating': 'Excellent',
                'color': 'bg-green-600',
                'description': 'Outstanding performance'
            }
        elif percentage >= 75:
            return {
                'grade': 'A',
                'rating': 'Very Good', 
                'color': 'bg-blue-600',
                'description': 'Very good performance'
            }
        elif percentage >= 65:
            return {
                'grade': 'B',
                'rating': 'Good',
                'color': 'bg-yellow-600',
                'description': 'Good performance'
            }
        elif percentage >= 50:
            return {
                'grade': 'C',
                'rating': 'Satisfactory',
                'color': 'bg-orange-600',
                'description': 'Satisfactory performance'
            }
        else:
            return {
                'grade': 'F',
                'rating': 'Needs Improvement',
                'color': 'bg-red-600',
                'description': 'Needs improvement'
            }

    @property
    def performance_color(self):
        """Get color for performance badge"""
        evaluation = self.evaluate_performance()
        return evaluation['color']

    @property
    def grade(self):
        """Get grade"""
        evaluation = self.evaluate_performance()
        return evaluation['grade']

    @property
    def performance_rating(self):
        """Get performance rating"""
        evaluation = self.evaluate_performance()
        return evaluation['rating']

# class AcademicRecord(models.Model):
#     SUBJECT_CHOICES = (
#         ('military_tactics', 'Military Tactics'),
#         ('weapon_training', 'Weapon Training'),
#         ('communication', 'Communication'),
#         ('leadership', 'Leadership'),
#         ('first_aid', 'First Aid'),
#         ('physical_training', 'Physical Training'),
#         ('general_knowledge', 'General Knowledge'),
#     )
    
#     soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE, related_name='academic_records')
#     exam_name = models.CharField(max_length=100)
#     subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
#     marks = models.FloatField()
#     total_marks = models.FloatField(default=100)
#     remarks = models.TextField(blank=True, null=True)
#     created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at', 'soldier']

#     def __str__(self):
#         return f"{self.soldier} - {self.exam_name} - {self.subject}"

#     @property
#     def percentage(self):
#         return (self.marks / self.total_marks) * 100 if self.total_marks else 0