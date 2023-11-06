from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Dance Dance API",
        default_version="v1",
        description="Dance Dance API v1.",
        contact=openapi.Contact(email="wogur981208@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API
    # Swagger
    path("swagger/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
