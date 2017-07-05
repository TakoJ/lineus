from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum
from django.db.models import Q
from .models import *
from staff.models import *
from staff.forms import RegisterForm,PT_RegisterForm,PT_Register_HistoryForm,Schedule_AddForm
from datetime import timedelta
import datetime
import json


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
    members = request.user.members.all() #member의 staff의 related_name='members'
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

def schedule(request): #스케줄 관리 페이지
    schedules = request.user.schedule.all() #나의 스케줄
    PT_members = request.user.PT_members.all() #나의 PT 회원들
    date = datetime.date.today() #오늘 받기
    context = {
        'PT_members' : PT_members,
        'date' : date,
        'schedules' : schedules,
    }
    return render(request, 'fitness/schedule.html', context)

def PT_member_detail(request, PT_member_id):
    PT_member = Member.objects.get(id=PT_member_id)
    member_history = History.objects.filter(user=PT_member).filter(birth=PT_member.birth) #이름과 생일 모두 일치하는 회원 기록만 불러오기

    context = {
        'PT_member' : PT_member,
        'member_history' : member_history,
    }
    return render(request, 'fitness/PT_member_detail.html', context)

def PT_member_delete(request, PT_member_id):
    # member = Member.objects.get(id=PT_member_id)
    for p in request.user.PT_members.filter(id=PT_member_id):
        #PT_register할때 했던 것들 다 null로 바꾸기
        p.Trainer = None
        p.registered_session = None
        p.PT_payment_amount = None
        p.PT_payment_method = None
        p.unitprice = None
        p.period_PT = None
        p.registered_date = None
        p.save()
    messages.info(request, 'PT회원이 삭제되었습니다.')
    return redirect('schedule')

def PT_register(request): #PT_register_list (회원리스트)
    member_list = Member.objects.all()
    context = {
        'member_list' : member_list,
    }
    return render(request, 'fitness/PT_register.html', context)

def PT_register_create(request, member_id):
    member = Member.objects.get(id=member_id)

    if request.method == 'POST':
        form = PT_RegisterForm(request.POST , instance=member)
        form1 = PT_Register_HistoryForm(request.POST or None)
        if form.is_valid() and form1.is_valid():
            member.Trainer=request.user
            form.save()
            #PT 등록 기록 남기기
            history = form1.save(commit=False)
            history.user = member.name
            history.birth = member.birth
            history.Trainer=request.user
            history.save()
            return redirect('schedule')


    else:
        form=PT_RegisterForm()
        form1 = PT_Register_HistoryForm()

    return render(request, 'fitness/PT_register_create.html',{
        'member' : member,
        'form':form,
        'form1':form1,
        })

def search(request):

    keyword = request.GET.get('q','') #검색 키워드

    # condition=(Q(성명__icontains=keyword))

    search_member = Member.objects.filter(name__icontains=keyword)#검색 조건 이름

    context= {
        'search_member' : search_member,
    }
    return render(request, 'fitness/search_result.html', context)


def schedule_add(request):
    if request.is_ajax():
        start_original = request.POST.get('start',None)
        s1 = start_original.split()[1:5] #korean standard time을 datetimefield 형식에 맞추기 위해 split ['Jul', '06','2017','08:00:00']
        s = ' '.join(s1) #split후 다시 합치기
        print(s)
        start= datetime.datetime.strptime(s, '%b %d %Y %H:%M:%S') #%T = %H:%M:%S
        end = datetime.datetime.strptime(s, '%b %d %Y %H:%M:%S')

        title = request.POST.get('title',None)
        member = Member.objects.get(id=request.POST.get('id')) #넘겨온 id의 회원 찾기
        Schedule.objects.create(
            Trainer=request.user,
            title = title, #받아온 data중 title 얻기
            start = start,
            end = end,
            birth= member.birth,
            )
        context={

        }
        messages.info(request, '스케줄이 등록었습니다.')
        context={
            'title':title,
        }

    else:
        context={
            'title':title,
        }
    return HttpResponse(json.dumps(context), content_type='application/json')
