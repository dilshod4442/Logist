from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from courses.views import home, about

urlpatterns = [
    path("admin/", admin.site.urls), path("", home, name="home"), path("about/", about, name="about"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("accounts.urls")), path("topics/", include("courses.urls")),
    path("materials/", include("materials.urls")), path("tests/", include("quizzes.urls")),
    path("glossary/", include("glossary.urls")), path("dashboard/", include("dashboard.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
