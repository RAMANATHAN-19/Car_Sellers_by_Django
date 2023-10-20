from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.saleslisting, name="saleslisting"),
    url(r'^add$', views.add, name="add"),
    url(r'^delete/(?P<id>\w{0,50})/$', views.delete, name="delete"),
    url(r'^order-details/(?P<id>\w{0,50})/$', views.order_details, name="order_details"),
    url(r'^delete/items/(?P<id>\w{0,50})/$', views.delete_oi, name="delete_oi"),
]

