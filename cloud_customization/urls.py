from django.urls import include, path
from . import views

urlpatterns = [
    path('api/backup/horilla-postgres-db', views.DatabaseBackupAPIView.as_view(), name=''),
    path('cloud/subscription-validity',views.CloudOrganizationView.as_view(),name='check_cloud_subscription_validity')
]                                                                                                                                                                               