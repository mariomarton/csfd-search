from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', views.search_view, name='search'),
    path('', views.search_view),
]