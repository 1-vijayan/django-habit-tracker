from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('study', 'Study'),
    ('fitness', 'Fitness'),
    ('health', 'Health'),
]


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='study'
    )

    streak = models.IntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('habit', 'date')