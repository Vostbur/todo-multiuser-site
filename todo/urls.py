from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('list/', views.list_todo, name='list'),
    path('completed/', views.completed_todo, name='completed'),
    path('add/', views.add_todo, name='add'),
    path('detail/<int:pk>/', views.detail_todo, name='detail'),
    path('detail/<int:pk>/complete/', views.complete_todo, name='complete'),
    path('detail/<int:pk>/delete/', views.delete_todo, name='delete'),
]
