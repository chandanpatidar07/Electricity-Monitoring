from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('signup/add_appliances/', views.add_appliances, name='add_appliances'),
    path('signup/add_appliances.html', RedirectView.as_view(url='/signup/add_appliances/', permanent=True)),
]
