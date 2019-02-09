# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 17:52:18 2019

@author: Casian
"""

from django.conf.urls import url
from rango import views

urlpatterns = [
        url(r'^$', views.index, name = 'index'),
        url(r'^about/', views.about, name = 'about'),
]