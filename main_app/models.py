from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Activity(models.Model):
    title = models.CharField(max_length =75)
    description = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('activity_detail', kwargs={'activity_id': self.id})

class Log(models.Model):
    date_completed = models.DateField('Date Completed')
    duration_in_minutes = models.IntegerField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.duration_in_minutes} completed on {self.date_completed}"

    class Meta:
        ordering = ['-date_completed']
