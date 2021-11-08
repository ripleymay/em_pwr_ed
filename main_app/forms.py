from django.forms import ModelForm
from .models import Activity, Log

class ActivityForm(ModelForm):
  class Meta:
    model = Activity
    fields = ['title', 'description', 'categories']

class LogForm(ModelForm):
  class Meta:
    model = Log
    fields = ['date_completed', 'duration_in_minutes']