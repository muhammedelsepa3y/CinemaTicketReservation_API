
from django.contrib import admin
from django.db import router
from rest_framework.routers import DefaultRouter
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('tickets.urls')),
]
