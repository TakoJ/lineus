from django.conf.urls import url, include
from django.contrib import admin
from management import views

urlpatterns = [
    url(r'^member_management/$', views.member_management, name='member_management'),
    url(r'^member_management/member_search/$', views.member_search, name='member_search'),
    url(r'^member_management/payment_history/(?P<member_id>\d+)/$', views.payment_history, name='payment_history'),
    url(r'^member_management/refund/(?P<history_id>\d+)/$', views.refund, name='refund'),
    url(r'^member_management/staff_mypage/(?P<staff_id>\d+)/$', views.staff_mypage, name='staff_mypage'),
    url(r'^member_management/staff_sales/(?P<staff_id>\d+)/$', views.staff_sales, name='staff_sales'),
    url(r'^member_management/edit_staff/(?P<staff_id>\d+)/$', views.edit_staff, name="edit_staff"),
    url(r'^member_management/edit_member/(?P<member_id>\d+)/$', views.edit_member, name="edit_member"),
    url(r'^member_management/delete_member/(?P<member_id>\d+)/$', views.delete_member, name="delete_member"),
    url(r'^member_management/delete_staff/(?P<staff_id>\d+)/$', views.delete_staff, name="delete_staff"),
    url(r'^schedule_management/$', views.schedule_management, name='schedule_management'),
    url(r'^schedule_management/staff_schedule/(?P<staff_id>\d+)', views.staff_schedule, name="staff_schedule"),
    url(r'^commission_management/$', views.commission_management, name='commission_management'),
    ##커미션 수정
    url(r'^commission_management/fc_teamleader_edit_com/(?P<fc_teamleader_id>\d+)/$', views.fc_teamleader_edit_com, name='fc_teamleader_edit_com'),
    url(r'^commission_management/fc_team_edit_com/(?P<fc_team_id>\d+)/$', views.fc_team_edit_com, name='fc_team_edit_com'),
    url(r'^commission_management/fc_personal_edit_com/(?P<fc_team_id>\d+)/$', views.fc_personal_edit_com, name='fc_personal_edit_com'),

    url(r'^commission_management/fit_teamleader_edit_com/(?P<fit_teamleader_id>\d+)/$', views.fit_teamleader_edit_com, name='fit_teamleader_edit_com'),
    url(r'^commission_management/fit_team_edit_com/(?P<fit_team_id>\d+)/$', views.fit_team_edit_com, name='fit_team_edit_com'),

    url(r'^commission_management/pil_teamleader_edit_com/(?P<pil_teamleader_id>\d+)/$', views.pil_teamleader_edit_com, name='pil_teamleader_edit_com'),
    url(r'^commission_management/pil_team_edit_com/(?P<pil_team_id>\d+)/$', views.pil_team_edit_com, name='pil_team_edit_com'),
    url(r'^commission_management/pil_pt_edit_com/(?P<fix_id>\d+)/$', views.pil_pt_edit_com, name='pil_pt_edit_com'),
    url(r'^commission_management/pil_dependingnum_edit_com/(?P<d_id>\d+)/$', views.pil_dependingnum_edit_com, name='pil_dependingnum_edit_com'),
    url(r'^commission_management/pil_gx_basic_edit_com/(?P<b_id>\d+)/$', views.pil_gx_basic_edit_com, name='pil_gx_basic_edit_com'),
    ##커미션 수정End
    url(r'^sales_management/$', views.sales_management, name='sales_management'),
    url(r'^set_today/$', views.set_today, name='set_today'),
    url(r'^sales_search/$', views.sales_search, name='sales_search'),
    ##fitenss 스케줄
    url(r'^Fitness_schedule_management/$', views.Fitness_schedule_management, name='Fitness_schedule_management'),
    #일일 근무 현황(피트니스)
    url(r'^fitness_daily_schedule/$', views.fitness_daily_schedule, name='fitness_daily_schedule'),
    url(r'^fitness_daily_schedule_search/$', views.fitness_daily_schedule_search, name='fitness_daily_schedule_search'),
    #일일 근무 현황(필라테스)
    url(r'^pilates_daily_schedule/$', views.pilates_daily_schedule, name='pilates_daily_schedule'),
    url(r'^pilates_daily_schedule_search/$', views.pilates_daily_schedule_search, name='pilates_daily_schedule_search'),
]