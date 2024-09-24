from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('download-music/', views.download_video, name='download_video'),
    path('start-download/', views.start_download, name='start_download'),
    # other paths
]

