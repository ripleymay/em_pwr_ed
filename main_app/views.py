from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Activity, Log
from .forms import ActivityForm

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def dashboard(request):
  categories = Category.objects.all()
  return render(request, 'categories/index.html', { 'categories': categories })  

class ActivityCreate(CreateView):
  model = Activity
  # fields = ['title', 'description', 'categories']
  form_class = ActivityForm
  # will be called if the cat data is valid
  def form_valid(self, form):
    # form.instance is the in-memory new cat obj
    form.instance.user = self.request.user
    # Let the CreateView's form_valid method do its job
    return super().form_valid(form)

class ActivityUpdate(UpdateView):
  model = Activity
  form_class = ActivityForm

class ActivityList(ListView):
  model = Activity

class ActivityDetail(DetailView):
  model = Activity

class ActivityDelete(DeleteView):
  model = Activity
  success_url = '/dashboard/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)