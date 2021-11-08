from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/<int:activity_id>/', views.activity_detail, name='activity_detail'),
    path('activities/create/', views.ActivityCreate.as_view(), name='activity_create'),
    path('activities/<int:pk>/update/', views.ActivityUpdate.as_view(), name='activity_update'),
    path('activities/<int:pk>/delete/', views.ActivityDelete.as_view(), name='activity_delete'),
    path('activities/<int:activity_id>/add_log', views.add_log, name='log_create'),
    path('activities/<int:activity_id>/delete_log/<int:log_id>', views.delete_log, name='log_delete')
]