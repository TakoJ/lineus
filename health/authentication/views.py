from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from authentication.forms import  StaffRegisterForm
from authentication.models import User, FC_Salary, Fitness_Salary, Pilates_Salary
from datetime import timedelta
from decimal import Decimal
import datetime
import json

def signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form= SignupForm()
    return render(request, 'signup.html', {
        'form':form,
        })

def staff_register(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management:member_management')
    else:
        form = StaffRegisterForm()

    context = {
        'form' : form
    }
    return render(request, 'staff_register.html', context)

def fc_salary_save(request):
    if request.is_ajax():
        today = datetime.date.today() #오늘 받기
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1) #이번달 1일에서 하루 빼기.그럼 저번 달
        lastMonth = lastMonth.replace(day=1)
        staff_id = request.POST.get('id',None)
        staff = User.objects.get(id=staff_id)
        team_members = User.objects.filter(groups__name='FC') #FC 팀 직원들


        FC_Salary.objects.create(
            uid = staff_id,
            user = staff,
            date = lastMonth,
            number = team_members.count()-1, #팀장제외.
            team_sales = Decimal(request.POST.get('team_sales', None).replace(",","")),
            personal_sales = Decimal(request.POST.get('personal_sales', None).replace(",","")),
            basic_salary = Decimal(request.POST.get('basic_salary', None).replace(",","")),
            commission_rate = float(request.POST.get('commission_rate', None)),
            commission = Decimal(request.POST.get('commission', None).replace(",","")),
            personal_commission_rate = float(request.POST.get('personal_commission_rate', None)),
            personal_commission = Decimal(request.POST.get('personal_commission', None).replace(",","")),
            total = Decimal(request.POST.get('total', None).replace(",","")),
            refund = Decimal(request.POST.get('refund', None)),
            salary = Decimal(request.POST.get('salary', None).replace(",","")),
            )
        context = {}
    else: #ajax아닐 시
        context={}
    return HttpResponse(json.dumps(context), content_type='application/json')

def fitness_salary_save(request):
    if request.is_ajax():
        today = datetime.date.today() #오늘 받기
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1) #이번달 1일에서 하루 빼기.그럼 저번 달
        lastMonth = lastMonth.replace(day=1)
        staff_id = request.POST.get('id',None)
        staff = User.objects.get(id=staff_id)


        Fitness_Salary.objects.create(
            uid = staff_id,
            user = staff,
            date = lastMonth,
            team_sales = Decimal(request.POST.get('team_sales', None).replace(",","")),
            personal_sales = Decimal(request.POST.get('personal_sales', None).replace(",","")),
            basic_salary = Decimal(request.POST.get('basic_salary', None).replace(",","")),
            commission_rate = float(request.POST.get('commission_rate', None)),
            commission = Decimal(request.POST.get('commission', None).replace(",","")),
            tuition_rate = int(request.POST.get('tuition_rate', None)),
            tuition = Decimal(request.POST.get('tuition', None).replace(",","")),
            total = Decimal(request.POST.get('total', None).replace(",","")),
            refund = Decimal(request.POST.get('refund', None)),
            salary = Decimal(request.POST.get('salary', None).replace(",","")),
            )
        context = {}
    else: #ajax아닐 시
        context={}
    return HttpResponse(json.dumps(context), content_type='application/json')

def pilates_salary_save(request):
    if request.is_ajax():
        today = datetime.date.today() #오늘 받기
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1) #이번달 1일에서 하루 빼기.그럼 저번 달
        lastMonth = lastMonth.replace(day=1)
        staff_id = request.POST.get('id',None)
        staff = User.objects.get(id=staff_id)


        Pilates_Salary.objects.create(
            uid = staff_id,
            user = staff,
            date = lastMonth,
            team_sales = Decimal(request.POST.get('team_sales', None).replace(",","")),
            personal_sales = Decimal(request.POST.get('personal_sales', None).replace(",","")),
            basic_salary = Decimal(request.POST.get('basic_salary', None).replace(",","")),
            commission_rate = float(request.POST.get('commission_rate', None)),
            commission = Decimal(request.POST.get('commission', None).replace(",","")),

            GX_commission = Decimal(request.POST.get('GX_commission', None).replace(",","")),
            PT_commission_rate = float(request.POST.get('PT_commission_rate', None)),
            PT_commission = Decimal(request.POST.get('PT_commission', None).replace(",","")),
            total = Decimal(request.POST.get('total', None).replace(",","")),
            refund = Decimal(request.POST.get('refund', None)),
            salary = Decimal(request.POST.get('salary', None).replace(",","")),
            )
        context = {}
    else: #ajax아닐 시
        context={}
    return HttpResponse(json.dumps(context), content_type='application/json')