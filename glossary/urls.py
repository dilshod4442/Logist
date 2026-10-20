from django.urls import path
from .views import term_list
urlpatterns = [path("", term_list, name="glossary")]
