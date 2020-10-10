# -*- coding: utf-8 -*-

from django.urls import path

from .views.account import login, register, validate
from .views.profile import profile_router
from .views.tab import tab_router, delete_tab
from .views.file import file_router


urlpatterns = [
    path('login', login),
    path('register', register),
    path('validate', validate),

    path('profile', profile_router),

    path('tab/<int:id>/delete', delete_tab),
    path('tab/<int:id>', tab_router),
    path('tab', tab_router),

    path('file', file_router),
    path('file/<str:id>', file_router),
]
