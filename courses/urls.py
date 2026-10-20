from django.urls import path
from . import views
urlpatterns = [path("", views.topic_list, name="topic-list"), path("lectures/", views.lectures, name="lectures"), path("practice/", views.practice, name="practice"), path("<slug:slug>/", views.topic_detail, name="topic-detail"), path("<slug:slug>/complete/", views.toggle_complete, name="toggle-complete")]
