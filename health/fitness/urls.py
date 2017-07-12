from django.conf.urls import url
from fitness import views

urlpatterns= [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^mypage/$', views.mypage, name='mypage'),
    url(r'^PT_mypage/$', views.PT_mypage, name='PT_mypage'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^schedule/PT_member_detail/(?P<PT_member_id>\d+)', views.PT_member_detail, name='PT_member_detail'),
    url(r'^schedule/PT_member_delete/(?P<PT_member_id>\d+)', views.PT_member_delete, name="PT_member_delete"),
    url(r'^schedule/PT_member_session_end/(?P<PT_member_id>\d+)', views.PT_member_session_end, name="PT_member_session_end"),
    url(r'^schedule/PT_register/$', views.PT_register, name='PT_register'),
    url(r'^schedule/PT_register/search/$', views.search, name='search'),
    url(r'^schedule/PT_register/(?P<member_id>\d+)', views.PT_register_create, name='PT_register_create'),
    url(r'^schedule_add/$', views.schedule_add, name='schedule_add'),
    url(r'^schedule_delete/(?P<schedule_id>\d+)', views.schedule_delete, name='schedule_delete'),

]