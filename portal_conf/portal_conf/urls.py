from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('audioconf.urls', namespace='audioconf')),
    path("admin/", admin.site.urls),
]
