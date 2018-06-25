from django.conf.urls import url
from . import views           # This line is new!


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/',views.register),
    url(r'^login/', views.login),
    url(r'^dashboard/', views.dashboard),
    url(r'^addJob/', views.addjob),
    url(r'^adding/', views.adding),
    url(r'^addtouser/(?P<numbers>\d+)$', views.addtouser),
    url(r'^view/(?P<numbers>\d+)$', views.view),
    url(r'^edit/(?P<numbers>\d+)$', views.edit),
    url(r'^editing/(?P<numbers>\d+)$', views.editing),
    url(r'^delete/(?P<numbers>\d+)$', views.delete),
    url(r'^clear/', views.clear)
]