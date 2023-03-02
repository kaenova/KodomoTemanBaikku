"""Mainsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Mainapp import views

urlpatterns = [
    path('', views.index),
    path('predict', views.predict),
    path('no_hate_speech', views.no_hate_speech),
    path('hate_speech/<str:id>', views.hate_speech),
    path('hate_speech_detail/<str:id>', views.hate_speech_detail),
]
