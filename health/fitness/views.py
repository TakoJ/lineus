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
    return render(request, 'home.html')

def register(request):
    # 받아온 데이터를 통해 레지스터폼 인스턴스 생성
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.staff=request.user #staff를 현재 유저로 저장한 뒤
            instance.save() #회원가입 저장

            messages.info(request, '회원가입이 되었습니다.')
            return render(request,'home.html') #완료후 홈 페이지로 로딩
    else:
        #post 요청이 아닐경우 빈 폰 인스턴스 생성
        form = RegisterForm()

    return render(request, 'register.html', {
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
    return render(request, 'mypage.html', context)

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

    return render(request, 'PT_mypage.html', context)

def schedule(request): #스케줄 관리 페이지
    schedules = request.user.schedule.all() #나의 스케줄
    PT_members = request.user.PT_members.all() #나의 PT 회원들
    date = datetime.date.today() #오늘 받기
    context = {
        'PT_members' : PT_members,
        'date' : date,
        'schedules' : schedules,
    }
    return render(request, 'schedule.html', context)

def PT_member_detail(request, PT_member_id):
    PT_member = Member.objects.get(id=PT_member_id)
    member_history = History.objects.filter(user=PT_member).filter(birth=PT_member.birth) #이름과 생일 모두 일치하는 회원 기록만 불러오기

    context = {
        'PT_member' : PT_member,
        'member_history' : member_history,
    }
    return render(request, 'PT_member_detail.html', context)

def PT_member_session_end(request, PT_member_id):
    p = Member.objects.get(id=PT_member_id)
    if p.re_registered==True: #재등록회원이라면
        for h in History.objects.filter(user=p.name).filter(birth=p.birth).filter(registered_date__gt=p.registered_date): #큰쪽이 더 최신날짜
        #해당회원의 히스토리중, 만료된 세션 등록일보다 더 최근에 등록한 히스토리를 찾는다.
            p.Trainer = h.Trainer
            p.registered_session = h.registered_session
            p.PT_payment_amount = h.PT_payment_amount
            p.PT_payment_method = h.PT_payment_method
            p.unitprice = h.unitprice
            p.period_PT = h.period_PT
            p.registered_date = h.registered_date
            p.re_registered = False #재등록여부는 다시 false로
            p.save()
    else: #재등록회원이 아니라면, pt등록정보 초기화
        p.Trainer = None
        p.registered_session = None
        p.PT_payment_amount = None
        p.PT_payment_method = None
        p.unitprice = None
        p.period_PT = None
        p.registered_date = None
        p.save()
    return redirect('schedule')

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
        p,re_registered = False
        p.save()
    messages.info(request, 'PT회원이 삭제되었습니다.')
    return redirect('schedule')

def PT_register(request): #PT_register_list (회원리스트)
    member_list = Member.objects.all()
    context = {
        'member_list' : member_list,
    }
    return render(request, 'PT_register.html', context)

def PT_register_create(request, member_id):
    member = Member.objects.get(id=member_id)

    if request.method == 'POST':
        form = PT_RegisterForm(request.POST , instance=member)
        form1 = PT_Register_HistoryForm(request.POST or None)
        if form.is_valid() and form1.is_valid():
            if member.Trainer != request.user: #재등록이 아니라면,
                member.Trainer = request.user
                member.registered_date = datetime.date.today() #오늘
                form.save()

            else: #재등록이라면 재등록여부를 true로 하기
                Member.objects.filter(id=member_id).update(re_registered=True)
                # 기본 멤버정보는 안바뀌고 PT 등록(history) 기록만 남기기

            history = form1.save(commit=False)
            history.user = member
            history.birth = member.birth
            history.Trainer=request.user
            check = History.objects.filter(user=member).filter(birth=member.birth) #그동안 몇번 pt등록했는지 확인
            if check.exists():
                history_num = check.count()
                history.Num = history_num + 1
            else:
                history.Num = 1

            history.save()
            return redirect('schedule')


    else: #POST요청이 아니라면
        form=PT_RegisterForm()
        form1 = PT_Register_HistoryForm()

    return render(request, 'PT_register_create.html',{
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
    return render(request, 'search_result.html', context)


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

        succeeding_schedule = Schedule.objects.filter(name=member).filter(birth=member.birth).filter(registered_date=member.registered_date).filter(start__gt=start).filter(~Q(title__icontains='예비')) #뒤에 있는 스케줄들


        if succeeding_schedule.exists(): #현재 추가하는 스케줄보다 뒤에 스케줄이 있다면
            first_succeeding_schedule = succeeding_schedule.latest('start') # 뒤에있는 것중, 가장 최근
            used_session = first_succeeding_schedule.used_session  # 현재 추가하는 스케줄의 사용된세션 = 가장 최근세션의 사용된세션

            for s in succeeding_schedule.order_by('start'): #시간에 따른 오림차순
                s.used_session = s.used_session + 1 #빠른세션들 사용된세션을 +1
                s.save()


            if '예비' in title: #예비 버튼이라면
                    member.used_session = member.used_session+0 #세션추가 없음
            else:
                member.used_session = member.used_session+1 #사용된 세션1회추가

            member.save() # +1 상태 저장

        else:  # 뒤에 스케줄이 없다면
            if '예비' in title: #예비 버튼이라면
                    member.used_session = member.used_session+0 #세션추가 없음
            else:
                member.used_session = member.used_session+1 #사용된 세션1회추가

            member.save() # +1 상태 저장

            used_session = member.used_session

        Schedule.objects.create(
            Trainer=request.user,
            name = member,
            title = title, #받아온 data중 title 얻기
            start = start,
            end = end,
            birth= member.birth,
            registered_date = member.registered_date,
            used_session = used_session,
            registered_session = member.registered_session,
            )
        context={
            'used_session':member.used_session,
        }

    else:
        context={
            'used_session':member.used_session,
        }
    return HttpResponse(json.dumps(context), content_type='application/json')

def schedule_delete(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id) #해당 스케줄찾기
    member = schedule.name #해당 회원 찾기

    succeeding_schedule = Schedule.objects.filter(name=member).filter(birth=member.birth).filter(registered_date=schedule.registered_date).filter(start__gt=schedule.start).filter(~Q(title__icontains='예비')) #같은 회원권 스케줄중(예비가 아닌), 빠른 날짜가 있는지 찾는다. 큰쪽이 더 최신날짜

    if succeeding_schedule.exists(): #현재 지우는 스케줄보다 뒤에 스케줄이 있다면
        for s in succeeding_schedule.order_by('start'): #시간에 따른 오림차순
            s.used_session = s.used_session - 1 #빠른세션들 사용된세션
            s.save()

    if '예비' in schedule.title : #예비 버튼이라면
            member.used_session = member.used_session+0 #세션삭제 없음
    else:
        member.used_session = member.used_session-1
        #스케줄 삭제시 세션 횟수도 하나 삭제.


    member.save() # +0 or -1 상태 저장
    schedule.delete() #스케줄 삭제

    return redirect('schedule')

def sales(request):
    return render(request, 'sales.html')
