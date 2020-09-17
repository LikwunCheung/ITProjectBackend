# -*- coding: utf-8 -*-

from django.urls import path

from ITProjectBackend.api.views.account import login, register, validate
from ITProjectBackend.api.views.profile import profile_router
from ITProjectBackend.api.views.tab import tab_router, delete_tab


urlpatterns = [
    path('login', login),
    path('register', register),
    path('validate', validate),

    path('profile', profile_router),

    path('tab/<int:id>/delete', delete_tab),
    path('tab/<int:id>', tab_router),
    path('tab', tab_router),
]
