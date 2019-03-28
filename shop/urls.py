from django.urls import re_path
from . import views

app_name = 'shop'
urlpatterns = [
	re_path(r'^$', views.index, name='index'),
	re_path(r'products/$', views.product_list, name='product_list'),
    re_path(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    re_path(r'^notes/(?P<note_slug>[-\w]+)/$',
        views.product_list_by_note,
        name='product_list_by_note'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),
    
]