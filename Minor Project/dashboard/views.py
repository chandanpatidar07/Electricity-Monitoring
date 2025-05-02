from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ApplianceUsage
import json

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error_message': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')
    else:
        return render(request, 'signup.html')

@login_required
def dashboard_view(request):
    appliances = ApplianceUsage.objects.filter(user=request.user)

    chart_data = {
        "labels": [a.appliance_name for a in appliances],
        "needed": [a.electricity_needed_kwh for a in appliances],
        "wasted": [a.electricity_wasted_kwh for a in appliances],
    }

    total_consumption = sum(a.electricity_needed_kwh + a.electricity_wasted_kwh for a in appliances)
    total_cost = sum(a.total_cost for a in appliances)
    efficiency = 0
    if total_consumption > 0:
        efficiency = (sum(a.electricity_needed_kwh for a in appliances) / total_consumption) * 100

    return render(request, 'dashboard.html', {
        'appliances': appliances,
        'chart_data': json.dumps(chart_data),
        'total_consumption': total_consumption,
        'total_cost': total_cost,
        'efficiency': round(efficiency, 2),
    })

@login_required
def add_appliances(request):
    if request.method == 'POST':
        appliance_names = request.POST.getlist('appliance_name[]')
        usage_times = request.POST.getlist('usage_time_hours[]')
        # For simplicity, set electricity_needed_kwh, electricity_wasted_kwh, cost_per_kwh to 0 or default values
        for i in range(len(appliance_names)):
            ApplianceUsage.objects.create(
                user=request.user,
                appliance_name=appliance_names[i],
                usage_time_hours=float(usage_times[i]) if i < len(usage_times) else 0,
                electricity_needed_kwh=0,
                electricity_wasted_kwh=0,
                cost_per_kwh=0,
            )
        return redirect('dashboard')
    else:
        return render(request, 'add_appliances.html')
