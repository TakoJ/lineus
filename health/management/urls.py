from django.conf.urls import url, include
from django.contrib import admin
from management import views

urlpatterns = [
    url(r'^member_management/$', views.member_management, name='member_management'),
    url(r'^member_management/edit_staff/(?P<staff_id>\d+)/$', views.edit_staff, name="edit_staff"),
    url(r'^member_management/edit_member/(?P<member_id>\d+)/$', views.edit_member, name="edit_member"),
    url(r'^member_management/delete_member/(?P<member_id>\d+)/$', views.delete_member, name="delete_member"),
    url(r'^member_management/delete_staff/(?P<staff_id>\d+)/$', views.delete_staff, name="delete_staff"),
    url(r'^schedule_management/$', views.schedule_management, name='schedule_management'),
    url(r'^schedule_management/staff_schedule/(?P<staff_id>\d+)', views.staff_schedule, name="staff_schedule"),
    url(r'^commission_management/$', views.commission_management, name='commission_management'),
    url(r'^commission_management/edit_commission/(?P<fc_teamleader_id>\d+)/$', views.edit_commission, name='edit_commission'),
    url(r'^sales_management/$', views.sales_management, name='sales_management'),
    url(r'^set_today/$', views.set_today, name='set_today'),
    url(r'^sales_search/$', views.sales_search, name='sales_search'),
]