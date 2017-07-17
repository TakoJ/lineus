from django.conf import settings
from django.conf.urls import url,include
from django.contrib.auth.views import login, logout
from authentication import views

urlpatterns = [
    # url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', login, name='login', kwargs={
        'template_name' : 'login.html',
        }),
    url(r'^logout/$', logout, name='logout', kwargs={
        'next_page': 'home.html',
        }),
    url(r'^staff_register/$', views.staff_register, name='staff_register'),
    url(r'^fc_salary_save/$', views.fc_salary_save, name='fc_salary_save'),
    url(r'^fitness_salary_save/$', views.fitness_salary_save, name='fitness_salary_save'),
    url(r'^pilates_salary_save/$', views.pilates_salary_save, name='pilates_salary_save'),

]