"""Blog_Project URL Configuration

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
from django.conf.urls import url
from blog.views import index, archive, tag, category, article, comment_post, do_logout, do_login, do_reg
from django.conf import settings

urlpatterns = [
    url(r'^upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    url(r'^archive/upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    url(r'^tag/upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^category/$', category, name='category'),
    url(r'^article/$', article, name='article'),
    url(r'^archive/$', archive, name='archive'),
    url(r'^tag/$', tag, name='tag'),
    url(r'^login/$', do_login, name='login'),
    url(r'^reg/$', do_reg, name='reg'),
    url(r'^logout/$', do_logout, name='logout'),
    url(r'^comment_post/$', comment_post, name='comment_post'),
    url(r'^$', index, name='index'),
]
