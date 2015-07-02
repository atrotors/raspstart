from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^history/$', views.ajax_history, name='ajax_history'),
  url(r'^submit/$', views.submit, name='submit'),
  url(r'^raspcheck/$', views.check, name='raspcheck'),
]
