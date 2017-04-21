from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^home$', views.home, name="home"),
    url(r'^add_task$', views.add_task, name="add_task"),
    url(r'logout', views.logout, name="logout"),
    url(r'^delete_task/(?P<id>\d+)', views.delete_task, name="delete_task"),
    url(r'^edit_task/(?P<id>\d+)', views.edit_task, name="edit_task"),
    url(r'^update_task/(?P<id>\d+)', views.update_task, name="update_task")
]