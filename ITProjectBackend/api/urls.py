# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('ITProjectBackend.api.urls_v1')),
]
