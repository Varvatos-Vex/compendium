from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('actor/<str:actor>', views.actor_details, name='actor_details'),
]