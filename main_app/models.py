from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORIES = (
    ('E', 'Emotional'),
    ('P', 'Physical'),
    ('SP', 'Spiritual'),
    ('SO', 'Social'),
    ('M', 'Mental'),
    ('En', 'Environmental'),
)

class Activity(models.Model):
    title = models.CharField(max_length =75)
    description = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
     return self.title

class Log(models.Model):
    date_completed = models.DateField('Date Completed')
    duration_in_minutes = models.IntegerField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.duration_in_minutes} completed on {self.date_completed}"

    class Meta:
        ordering = ['-date']

class Catagory(models.Model):
    pass