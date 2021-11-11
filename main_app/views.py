from django.shortcuts import render, redirect
from django.db.models import Sum
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Activity, Log
from .forms import LogForm
import datetime
import requests
import os

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def dashboard(request):
  key = os.environ['ZEN_API_KEY']
  quote = requests.get(f'https://zenquotes.io/api/today/{key}').json()

  categories = Category.objects.all()

  today = datetime.date.today()
  week_ago = today - datetime.timedelta(days=6)
  logs = Log.objects.filter(activity__user=request.user, date_completed__range=(week_ago, today))
  agg_logs = logs.values('activity__categories').annotate(mins=Sum('duration_in_minutes')).order_by()

  totals = []
  for ag in agg_logs:
    title = list(filter(lambda cat: cat.id == ag['activity__categories'], categories))[0].title
    totals.append({'title': title, 'mins': ag['mins']})

  return render(request, 'categories/index.html', { 
    'categories': categories, 
    'totals': totals, 
    'html': quote[0]['h'] 
  })  

class ActivityCreate(LoginRequiredMixin, CreateView):
  model = Activity
  fields = ['title', 'description', 'categories']
  # will be called if the activity data is valid
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ActivityUpdate(LoginRequiredMixin, UpdateView):
  model = Activity
  fields = ['title', 'description', 'categories']

class ActivityDelete(LoginRequiredMixin, DeleteView):
  model = Activity
  success_url = '/dashboard/'

@login_required
def activity_list(request):
  categories = Category.objects.all()
  category = request.GET.get('category')
  if category:
    activities = Activity.objects.filter(user=request.user, categories__title=category)
  else:
    activities = Activity.objects.filter(user=request.user)
  return render(request, 'activities/index.html', { 
    'categories': categories,
    'activities': activities, 
    'category': category
  })

@login_required
def activity_detail(request, activity_id):
  activity = Activity.objects.get(id=activity_id)
  log_form = LogForm()

  today = datetime.date.today()
  week_ago = today - datetime.timedelta(days=6)
  month_ago = today - datetime.timedelta(days=29)
  last_week_logs = Log.objects.filter(activity=activity, date_completed__range=(week_ago, today))
  last_month_logs = Log.objects.filter(activity=activity, date_completed__range=(month_ago, week_ago))
  all_prior_logs = Log.objects.filter(activity=activity, date_completed__lt=(month_ago))

  return render(request, 'activities/detail.html', {
    'activity': activity,
    'last_week_logs': last_week_logs,
    'last_month_logs': last_month_logs,
    'all_prior_logs': all_prior_logs,
    'log_form': log_form,
  })

@login_required
def add_log(request, activity_id):
  # create a ModelForm instance using the data in the posted form
  form = LogForm(request.POST)
  # validate the data
  if form.is_valid():
    new_log = form.save(commit=False)
    new_log.activity_id = activity_id
    new_log.save()
  return redirect('activity_detail', activity_id=activity_id)

@login_required
def delete_log(request, activity_id, log_id):
  Log.objects.filter(id=log_id).delete()
  return redirect('activity_detail', activity_id=activity_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

  