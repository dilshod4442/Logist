from django.urls import path
from . import views
urlpatterns = [path("", views.quiz_list, name="quiz-list"), path("<int:pk>/start/", views.start, name="quiz-start"), path("attempt/<int:pk>/", views.take, name="quiz-take"), path("attempt/<int:pk>/result/", views.result, name="quiz-result")]
