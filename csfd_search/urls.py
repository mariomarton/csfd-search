from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', views.search_view, name='search'),
    path('<str:model_name>/<int:pk>/', views.detail_view, name='detail'),
    path('', views.search_view),
]

handler404 = views.page_not_found_view
handler500 = views.server_error_view
