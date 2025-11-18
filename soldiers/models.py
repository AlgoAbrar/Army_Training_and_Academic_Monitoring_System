from django.db import models
from users.models import User

class Soldier(models.Model):
    RANK_CHOICES = (
        ('recruit', 'Recruit'),
        ('private', 'Private'),
        ('corporal', 'Corporal'),
        ('sergeant', 'Sergeant'),
        ('staff_sergeant', 'Staff Sergeant'),
        ('officer', 'Officer'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='soldier_profile')
    soldier_id = models.CharField(max_length=20, unique=True)
    rank = models.CharField(max_length=20, choices=RANK_CHOICES, default='recruit')
    unit = models.CharField(max_length=100)
    joining_date = models.DateField()
    assigned_trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                       related_name='trained_soldiers', limit_choices_to={'role': 'trainer'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.soldier_id} - {self.user.get_full_name() or self.user.username}"