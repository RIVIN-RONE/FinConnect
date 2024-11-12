from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path('', include('finance_app.urls')),  # Include the app-level URLs
]
