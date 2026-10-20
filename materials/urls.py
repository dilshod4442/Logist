from django.urls import path
from . import views
urlpatterns = [path("", views.material_list, name="material-list"), path("<int:pk>/download/", views.download, name="material-download"), path("video/<int:pk>/stream/", views.stream_video, name="video-stream"), path("file-video/<int:pk>/stream/", views.stream_material_video, name="material-video-stream")]
