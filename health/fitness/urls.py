from django.conf.urls import url
from fitness import views

urlpatterns= [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^re_register/$', views.re_register, name='re_register'),
    url(r'^re_register_search/$', views.re_register_search, name='re_register_search'),
    url(r'^re_register_create/(?P<member_id>\d+)/$', views.re_register_create, name='re_register_create'),
    url(r'^date_add/$', views.date_add, name='date_add'),
    url(r'^member_list/$', views.member_list, name='member_list'),
    url(r'^member_list/member_search/$', views.member_search, name='member_search'),
    url(r'^member_list/ot_member_search/$', views.ot_member_search, name='ot_member_search'),
    url(r'^member_list/member_history/(?P<member_id>\d+)/$', views.member_history, name='member_history'),
    url(r'^member_detail/(?P<member_id>\d+)/$', views.member_detail, name='member_detail'),
    url(r'^add_locker/(?P<member_id>\d+)/$', views.add_locker, name='add_locker'),
    url(r'^mypage/(?P<staff_id>\d+)/$', views.mypage, name='mypage'),
    url(r'^PT_mypage/(?P<staff_id>\d+)/$', views.PT_mypage, name='PT_mypage'),
    url(r'^Pilates_mypage/(?P<staff_id>\d+)/$', views.Pilates_mypage, name='Pilates_mypage'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^schedule/PT_member_detail/(?P<PT_member_id>\d+)', views.PT_member_detail, name='PT_member_detail'),
    url(r'^schedule/PT_member_delete/(?P<PT_member_id>\d+)', views.PT_member_delete, name="PT_member_delete"),
    url(r'^schedule/PT_member_session_end/(?P<PT_member_id>\d+)', views.PT_member_session_end, name="PT_member_session_end"),
    url(r'^schedule/PT_register/$', views.PT_register, name='PT_register'),
    url(r'^schedule/PT_register/search/$', views.search, name='search'),
    url(r'^schedule/PT_register/(?P<member_id>\d+)', views.PT_register_create, name='PT_register_create'),
    url(r'^schedule/Pil_register/(?P<member_id>\d+)', views.Pil_register_create, name='Pil_register_create'),
    url(r'^schedule_add/$', views.schedule_add, name='schedule_add'),
    url(r'^OT_schedule_add/$', views.OT_schedule_add, name='OT_schedule_add'),
    url(r'^schedule_delete/(?P<schedule_id>\d+)', views.schedule_delete, name='schedule_delete'),
    url(r'^purchasing_application/$', views.purchasing_application, name='purchasing_application'),

]