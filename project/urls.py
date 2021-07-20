from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from wagtail.admin import urls as wagtailadmin_urls
from django.conf.urls import include, re_path, url

from app.urls import schema_view

urlpatterns = [
    path('api/v1/', include('app.urls')),
    path('admin/', admin.site.urls),
    re_path(r'', include(wagtailadmin_urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
