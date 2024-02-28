from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="Bank Manager Rest API",
      default_version='v1',
      description="Bank Manager Rest API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="riquejdc@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/auth/', include('authentication.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/', include('manager.urls')),
    path('swagger<format>.json|.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
