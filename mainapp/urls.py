from django.urls import path, re_path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp.index, name='index'),

    re_path(r'^catalog/$', mainapp.catalog, name='catalog'),
    re_path(r'^categories/(?P<pk>\d+)/$', mainapp.catalog, name='category'),
    re_path(r'^categories/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp.catalog, name='category'),


    re_path(r'^product/?P<pk>(\d+)/$', mainapp.product, name='product'),

    re_path(r'^contacts/$', mainapp.contacts, name='contacts'),
    re_path(r'^conference/$', mainapp.conference, name='conference'),

]

