from django.forms import ModelForm
from .models import Activity, Log

class LogForm(ModelForm):
  class Meta:
    model = Log
    fields = ['date_completed', 'duration_in_minutes']