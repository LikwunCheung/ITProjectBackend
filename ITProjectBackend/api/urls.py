# -*- coding: utf-8 -*-

from django.urls import path, include

urlpatterns = [
    path('v1/', include('ITProjectBackend.api.urls_v1')),
]
