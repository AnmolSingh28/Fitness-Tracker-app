# models.py
from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=100, blank=True, null=True)
 

    def __str__(self):
        return self.name

class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise_name = models.CharField(max_length=100)
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.PositiveIntegerField()



# Create your models here.
