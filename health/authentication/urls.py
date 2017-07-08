from django.conf import settings
from django.conf.urls import url,include
from django.contrib.auth.views import login, logout
from authentication import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', login, name='login', kwargs={
        'template_name' : 'login.html',
        }),
    url(r'^logout/$', logout, name='logout', kwargs={
        'next_page': 'home.html',
        }),
]