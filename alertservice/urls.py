from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

# from cryptoalerts.alertservice import views
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'alerts', views.AlertViewSet, basename='alert')

urlpatterns = [
    path('', include(router.urls)),
    path('alerts/create/', views.AlertViewSet.as_view({'post': 'create_alert'}), name='create_alert'),
    path('alerts/delete/<int:alert_pk>/', views.AlertViewSet.as_view({'delete': 'delete_alert'}), name='delete_alert'),
]