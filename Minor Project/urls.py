from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', include('dashboard.urls')),  # Include the dashboard app's URLs
]
