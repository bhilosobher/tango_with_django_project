# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 17:52:18 2019

@author: Casian
"""

from django.conf.urls import url
from rango import views

#could namespace the rango urls, in case you have several apps (which could have same urls)
#app_name = 'rango'
urlpatterns = [
        url(r'^$', views.index, name = 'index'),
        url(r'^about/', views.about, name = 'about'),
        url(r'add_category/$', views.add_category, name= 'add_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', 
            views.show_category, name = 'show_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', 
            views.add_page, name = 'add_page'),
        url(r'^register/$', views.register, name = 'register'),
        url(r'^login/$', views.user_login, name = 'login' ),
        url(r'^logout/$', views.user_logout, name = 'logout'),
        url(r'^restricted/$', views.restricted, name='restricted'),
]