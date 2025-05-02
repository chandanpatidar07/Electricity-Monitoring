from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # Dashboard homepage
    path('signup/', views.signup, name='signup'),  # Signup page
    path('add-appliances/', views.add_appliances, name='add_appliances'),  # Add Appliances page
]
