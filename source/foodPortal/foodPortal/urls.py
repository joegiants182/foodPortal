"""foodPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from foodPortalApp.views import users
from foodPortalApp.views import menus
from foodPortalApp.views import items
from foodPortalApp.views import orders

urlpatterns = [ 
    # Examples:
    # url(r'^$', 'foodPortal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', users.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', users.login),
    url(r'^logout/', users.logout),
    url(r'^home/', users.home),

    url(r'^menus/all/', menus.all),
    url(r'^menus/add/', menus.add),
    url(r'^menus/addSection/(?P<id>\d+)/', menus.addSection),
    url(r'^menus/editSection/(?P<id>\d+)/', menus.editSection),
    url(r'^menus/(?P<id>\d+)/', menus.view),
    url(r'^menus/(?P<id>\d+)/disable/', menus.disable),
    url(r'^menus/(?P<id>\d+)/enable/', menus.enable),

    url(r'^items/addItem/(?P<id>\d+)/', items.addItem),
    url(r'^items/editItem/(?P<id>\d+)/', items.editItem),
    url(r'^items/addOption/(?P<id>\d+)/', items.addOption),
    url(r'^items/editOptions/(?P<id>\d+)/', items.editOptions),

    url(r'^orders/addTo/(?P<id>\d+)/', orders.addTo),
    url(r'^orders/view/', orders.view),
    url(r'^orders/update/(?P<id>\d+)/', orders.update),
    url(r'^orders/removeItem/(?P<id>\d+)/', orders.removeItem),
    ]
