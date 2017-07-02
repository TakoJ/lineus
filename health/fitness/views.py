from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum
from django.db.models import Q
from .models import *
from staff.models import *
from staff.forms import RegisterForm,PT_RegisterForm
from datetime import timedelta
import datetime


def home(request):
    #첫 화면
    return render(request, 'fitness/home.html')

def register(request):
    # 받아온 데이터를 통해 레지스터폼 인스턴스 생성
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.staff=request.user #staff를 현재 유저로 저장한 뒤
            instance.save() #회원가입 저장

            messages.info(request, '회원가입이 되었습니다.')
            return render(request,'fitness/home.html') #완료후 홈 페이지로 로딩
    else:
        #post 요청이 아닐경우 빈 폰 인스턴스 생성
        form = RegisterForm()

    return render(request, 'fitness/register.html', {
        'form': form,
        })

def mypage(request):
    members = request.user.members.all()
    date = datetime.date.today() #오늘 받기
    #####오늘#####
    today_members = members.filter(start_date=date) #오늘 등록한 회원
    today_members_pay = today_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00)
    #####이번주####
    start_week = date- datetime.timedelta(date.weekday()) #이번주(월요일시작)
    end_week = start_week + datetime.timedelta(6) #월요일 + 6 (일요일)
    this_month = datetime.timedelta(date.month)
    thisweek_members = members.filter(start_date__range=[start_week, end_week])
    thisweek_members_pay = thisweek_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00)
    ####이번달####
    this_month_start = datetime.datetime(date.year, date.month, 1)
    thismonth_members = members.filter(start_date__range=[this_month_start, date])
    thismonth_members_pay = thismonth_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00)
    context={
        'members' : members,
        'today_members' : today_members,
        'today_members_pay' : today_members_pay,
        'thisweek_members' : thisweek_members,
        'thisweek_members_pay' :thisweek_members_pay,
        'thismonth_members' : thismonth_members,
        'thismonth_members_pay' : thismonth_members_pay,
    }
    return render(request, 'fitness/mypage.html', context)

def PT_mypage(request):
    PT_members = request.user.PT_members.all()
    date = datetime.date.today() #오늘 받기
    #####오늘#####
    today_members = PT_members.filter(start_date=date) #오늘 등록한 회원
    today_members_pay = today_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00)
    #####이번주####
    start_week = date- datetime.timedelta(date.weekday()) #이번주(월요일시작)
    end_week = start_week + datetime.timedelta(6) #월요일 + 6 (일요일)
    this_month = datetime.timedelta(date.month)
    thisweek_members = PT_members.filter(start_date__range=[start_week, end_week])
    thisweek_members_pay = thisweek_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00)
    ####이번달####
    this_month_start = datetime.datetime(date.year, date.month, 1)
    thismonth_members = PT_members.filter(start_date__range=[this_month_start, date])
    thismonth_members_pay = thismonth_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00)
    context={
        'PT_members' : PT_members,
        'today_members' : today_members,
        'today_members_pay' : today_members_pay,
        'thisweek_members' : thisweek_members,
        'thisweek_members_pay' :thisweek_members_pay,
        'thismonth_members' : thismonth_members,
        'thismonth_members_pay' : thismonth_members_pay,
    }

    return render(request, 'fitness/PT_mypage.html', context)

def schedule(request):
    PT_members = request.user.PT_members.all()
    context = {
        'PT_members' : PT_members,
    }
    return render(request, 'fitness/schedule.html', context)

def PT_member_delete(request, PT_member_id):
    # member = Member.objects.get(id=PT_member_id)
    for p in request.user.PT_members.filter(id=PT_member_id):
        p.Trainer = None
        p.save()
    messages.info(request, 'PT회원이 삭제되었습니다.')
    return redirect('schedule')

def PT_register(request):
    member_list = Member.objects.all()
    context = {
        'member_list' : member_list,
    }
    return render(request, 'fitness/PT_register.html', context)

def PT_register_create(request, member_id):
    member = Member.objects.get(id=member_id)

    if request.method == 'POST':
        form = PT_RegisterForm(request.POST , instance=member)
        if form.is_valid():
            member.Trainer=request.user
            form.save()
            return redirect('schedule')

    else:
        form=PT_RegisterForm()

    return render(request, 'fitness/PT_register_create.html',{
        'member' : member,
        'form':form,
        })

def search(request):

    keyword = request.GET.get('q','') #검색 키워드

    # condition=(Q(성명__icontains=keyword))

    search_member = Member.objects.filter(name__icontains=keyword)#검색 조건 이름

    context= {
        'search_member' : search_member,
    }
    return render(request, 'fitness/search_result.html', context)
