from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.main.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.main.urls")),
    path("projects/", include("apps.portfolio.urls")),
    path("crm/", include("apps.crm.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
