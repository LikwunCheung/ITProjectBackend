# -*- coding: utf-8 -*-

from django.urls import path

from ITProjectBackend.api.views.account import login, register, validate


urlpatterns = [
    path('login', login),
    path('register', register),
    path('validate', validate),

    # path('profile',),
    #
    # path('tab/<id:int>/delete',),
    # path('tab/<id:int>',),
    # path('tab',),
]
