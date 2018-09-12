"""DownWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from CMDB import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('cmdbindex/', views.CMDBIndex)
    path('login/', views.login),
    path('host_manager/', views.host_manager),
    path('del_host/', views.del_host),
    path('detail/', views.detail),
    path('applications/', views.applications),
    path('delete_app/', views.delete_app),
    path('edit_app/', views.edit_app)

]
