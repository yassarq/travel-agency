from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^createtrip$', views.createtrip),
    url(r'^show/(?P<trip_id>\d+)$', views.show),
    url(r'^join/(?P<trip_id>\d+)$', views.join)
    


]
