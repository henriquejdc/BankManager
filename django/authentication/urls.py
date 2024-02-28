# Django imports
from django.urls import path
from . import views

urlpatterns = [
    path('health', views.HealthAuthView.as_view(), name='health_auth'),
    path('signup/', views.UserCreateView.as_view(), name='sign_up'),
]
