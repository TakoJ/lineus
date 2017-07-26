from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum
from django.db.models import Q
from .models import *
from staff.models import *
from management.models import *
from authentication.models import User, FC_Salary
from staff.forms import RegisterForm, Re_RegisterForm, MembershipHistoryForm, PT_RegisterForm,PT_Register_HistoryForm, Pil_RegisterForm, Pil_Register_HistoryForm
from management.forms import EditForm
from datetime import timedelta
import datetime
import json


def home(request):
    #첫 화면
    return render(request, 'home.html')

def register(request):
    today = datetime.date.today() #오늘 받기
    # 받아온 데이터를 통해 레지스터폼 인스턴스 생성
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        form1 = MembershipHistoryForm(request.POST or None)
        if form.is_valid() and form1.is_valid():
            instance =form.save(commit=False)
            instance.staff=request.user #staff를 현재 유저로 저장한 뒤
            instance.division = "신규"
            instance.save() #회원가입 저장

            history = form1.save(commit=False)
            history.user = instance
            history.birth = instance.birth
            history.division = "신규"
            history.staff = request.user
            history.save()

            PaymentHistory.objects.create(
                user = instance,
                division = 'Membership',
                date = instance.registered_date,
                start_date = instance.start_date,
                end_date = instance.end_date,
                payment_amount = instance.payment_amount
            )

            messages.info(request, '회원가입이 되었습니다.')
            return render(request,'home.html') #완료후 홈 페이지로 로딩
    else:
        #post 요청이 아닐경우 빈 폰 인스턴스 생성
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form,
        'today' : str(today),
        })

def re_register(request):
    return render(request, 're_register.html')


def re_register_search(request):

    keyword = request.GET.get('q','') #검색 키워드
    condition=(Q(name__icontains=keyword) | Q(phone_num__icontains=keyword))
    search_member = Member.objects.filter(condition)#검색 조건 이름, 휴대번호
    context= {
        'search_member' : search_member,
        'q' : keyword,
    }
    return render(request, 're_register.html', context)

def re_register_create(request, member_id):
    today = datetime.date.today() #오늘 받기
    member = Member.objects.get(id=member_id)
    member.Membership_status = 1
    member.save()

    if request.method == 'POST':
        form = Re_RegisterForm(request.POST, instance=member)
        history_form = MembershipHistoryForm(request.POST or None)
        if form.is_valid() and history_form.is_valid():
            instance =form.save(commit=False)
            instance.staff=request.user #staff를 현재 유저로 저장한 뒤
            instance.division = "재등록"
            instance.save()

            history = history_form.save(commit=False)
            history.division = "재등록"
            history.user = member
            history.birth = member.birth
            history.staff = request.user
            history.save() #회원권내역 생성

            PaymentHistory.objects.create(
                user = instance,
                division = 'Membership',
                date = instance.registered_date,
                start_date = instance.start_date,
                end_date = instance.end_date,
                payment_amount = instance.payment_amount
            )

            messages.info(request, '회원 재등록이 되었습니다.')
            return render(request,'home.html') #완료후 홈 페이지로 로딩

    else:
        form = Re_RegisterForm()
        history_form = MembershipHistoryForm()

    context = {
        'member' : member,
        'form':form,
        'history_form' : history_form,
        'today':str(today),
        'member_birth' : str(member.birth),
    }
    return render(request, 're_register_create.html', context)


def date_add(request):
    if request.is_ajax():
        start_date = request.POST.get('start_date',None)
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        d = int(request.POST.get('day',None))
        days = timedelta(days=d);
        end_date = start_date + days;
        context={
                'end_date':str(end_date),
            }

    else:
        context={

        }
    return HttpResponse(json.dumps(context), content_type='application/json')


def member_list(request):
    order_by = request.GET.get('order_by', 'name')
    members = Member.objects.all().order_by(order_by)
    context = {
        'members' : members,
    }
    return render(request, 'member_list.html', context)


def member_search(request):

    keyword = request.GET.get('q','') #검색 키워드

    condition=(Q(name__icontains=keyword) | Q(phone_num__icontains=keyword))

    search_member = Member.objects.filter(condition)#검색 조건 이름, 휴대번호

    context= {
        'search_member' : search_member,
        'q' : keyword,
    }
    return render(request, 'member_search.html', context)

def ot_member_search(request):
    # if request.is_ajax():
    keyword = request.GET.get('q','') #검색 키워드
    condition=(Q(name__icontains=keyword) | Q(phone_num__icontains=keyword))
    search_member = Member.objects.filter(condition)#검색 조건 이름, 휴대번호

    schedules = request.user.schedule.filter(~Q(title__icontains='OT')) #OT를 제외한 나의 스케줄
    OT_schedules = request.user.schedule.filter(title__icontains='OT') #OT 스케줄
    PT_members = request.user.PT_members.all() #나의 PT 회원들

    context= {
        'schedules':schedules,
        'OT_schedules':OT_schedules,
        'PT_members':PT_members,
        'search_member' : search_member,
        'q' : keyword,
    }
    return render(request, 'schedule.html', context)

def member_detail(request, member_id):
    member = Member.objects.get(id=member_id)
    form = EditForm(request.POST or None, instance=member)
    context = {
        'member' : member,
        'form' : form,
    }
    return render(request, 'member_detail.html', context)

def mypage(request, staff_id): # FC팀의 마이페이지
    thismonth_members_num = int(0)
    thismonth_members_pay = int(0)
    staff = User.objects.get(id=staff_id)
    members = staff.history_members.all() #memberhistory의 staff의 related_name='history_members'
    date = datetime.date.today() #오늘 받기
    #####오늘#####
    today_members = members.filter(registered_date=date) #오늘 등록한 회원
    today_members_pay = today_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00)
    #####이번주####
    start_week = date- datetime.timedelta(date.weekday()) #이번주(월요일시작)
    end_week = start_week + datetime.timedelta(6) #월요일 + 6 (일요일)
    this_month = datetime.timedelta(date.month)
    thisweek_members = members.filter(registered_date__range=[start_week, end_week])
    thisweek_members_pay = thisweek_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00)
    ####이번달####
    this_month_start = datetime.datetime(date.year, date.month, 1)
    thismonth_members = members.filter(registered_date__range=[this_month_start, date])
    thismonth_members_pay = thismonth_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00) if thismonth_members else 0

    ###저번달
    if date.month == 1: #1월이면, 작년 12월 return
        year = date.year-1
        last_month= 12
    else:
        year = date.year
        last_month = date.month-1

    lastmonth_members = members.filter(registered_date__year=year).filter(registered_date__month=last_month)
    lastmonth_members_pay = lastmonth_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00) if lastmonth_members else 0
    ########커미션#########
    last_team_sales_before = int(0)
    this_team_sales_before = int(0)
    basic_salary = staff.basic_salary
    team_members = User.objects.filter(groups__name='FC') #FC 팀 직원들

    for f in team_members:
        members = f.history_members.all()
        last_members = members.filter(registered_date__year=year).filter(registered_date__month=last_month) #지난달 등록한 회원들
        members_pay = last_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00) if last_members else 0 #Suspect some of members is None
        last_team_sales_before = last_team_sales_before + members_pay #저번달 팀 총 매출

        this_members = members.filter(registered_date__year=year).filter(registered_date__month=date.month) #이번달 등록한 회원들
        this_members_pay = this_members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00) if this_members else 0 #Suspect some of members is None
        this_team_sales_before = this_team_sales_before + this_members_pay # 이번달 팀 총 매출



    ######################환불############

    last_refund_list = RefundHistory.objects.none()
    this_refund_list = RefundHistory.objects.none()
    for m in staff.members.all(): #나의 회원만.
        payment = m.PaymentHistory.filter(division="Membership")
        for p in payment:
            try:
                last_refund = RefundHistory.objects.filter(payment=p).filter(refund_date__year=year).filter(refund_date__month=last_month)
                last_refund_list |= last_refund

                this_refund = RefundHistory.objects.filter(payment=p).filter(refund_date__range=[this_month_start, date])
                this_refund_list |= this_refund
            except:
                pass
    last_refund_list = last_refund_list.distinct()
    this_refund_list = this_refund_list.distinct()

    last_personal_refund = int(0)
    for i in last_refund_list:
        last_personal_refund = last_personal_refund + i.refund_amount #지난달 나의 회원 총 환불.

    this_personal_refund = int(0)
    for i in this_refund_list:
        this_personal_refund = this_personal_refund + i.refund_amount #이번달 나의 회원 총 환불.

    last_FC_refund = RefundHistory.objects.filter(division="Membership").filter(refund_date__year=year).filter(refund_date__month=last_month)  #지난달 회원권 총 환불.

    last_FC_refund_amount = last_FC_refund.aggregate(Sum('refund_amount')).get('refund_amount__sum',0.00) if last_FC_refund else 0 #Suspect some of members

    this_FC_refund = RefundHistory.objects.filter(division="Membership").filter(refund_date__range=[this_month_start, date]) #이번달 회원권 총 환불.

    this_FC_refund_amount = this_FC_refund.aggregate(Sum('refund_amount')).get('refund_amount__sum',0.00) if this_FC_refund else 0 #Suspect some of members

    #######환불End####################
    #
    ######총매출 - 환불##############
    #지난달
    last_team_sales = last_team_sales_before - last_FC_refund_amount
    if last_team_sales <0:
        last_team_sales=0

    lastmonth_members_pay_before = lastmonth_members_pay
    lastmonth_members_pay = lastmonth_members_pay_before - last_personal_refund
    if lastmonth_members_pay < 0:
        lastmonth_members_pay=0

    ## 이번달 FC팀 총 매출 - 이번달 FC팀 환불
    this_team_sales = this_team_sales_before - this_FC_refund_amount
    if this_team_sales < 0 :
        this_team_sales =0

    # 이번달 나의 총 매출 - 이번달 나의 환불
    thismonth_members_pay_before = thismonth_members_pay
    thismonth_members_pay = thismonth_members_pay_before - this_personal_refund
    if thismonth_members_pay < 0:
        thismonth_members_pay = 0

    ######총매출 - 환불 End###########

    #팀장이면
    if staff.teamleader == True:
        last_commissions = FC_Teamleader_Commission.objects.filter(min_sales__lte=last_team_sales).filter(max_sales__gt=last_team_sales)
        this_commissions = FC_Teamleader_Commission.objects.filter(min_sales__lte=this_team_sales).filter(max_sales__gt=this_team_sales)

        last_personal_commission_rate = float(0)
        last_personal_commission = float(0)
        this_personal_commission_rate = float(0)
        this_personal_commission = float(0)

     #팀원이면
    else:
        last_commissions = FC_Team_Commission.objects.filter(min_sales__lte=last_team_sales).filter(max_sales__gt=last_team_sales)
        this_commissions = FC_Team_Commission.objects.filter(min_sales__lte=this_team_sales).filter(max_sales__gt=this_team_sales)

        last_personal_commissions = FC_Personal_Commission.objects.filter(min_personal_sales__lte =lastmonth_members_pay).filter(max_personal_sales__gt=lastmonth_members_pay).filter(personnel=team_members.count()-1) #팀장제외 팀원들 인원 필터링
        this_personal_commissions = FC_Personal_Commission.objects.filter(min_personal_sales__lte =thismonth_members_pay).filter(max_personal_sales__gt=thismonth_members_pay).filter(personnel=team_members.count()-1)

        for pc in last_personal_commissions:
            last_personal_commission_rate = pc.commission

        last_personal_commission = int(lastmonth_members_pay) * last_personal_commission_rate/100

        for pc in this_personal_commissions:
            this_personal_commission_rate = pc.commission

        this_personal_commission = int(thismonth_members_pay) * this_personal_commission_rate/100

    #팀장, 팀원 공통
    for c in last_commissions:
        last_commission_rate = c.commission

    last_commission = float(last_team_sales) * last_commission_rate/100

    for c in this_commissions:
        this_commission_rate = c.commission

    this_commission = float(this_team_sales) * this_commission_rate/100

    last_total = int(staff.basic_salary) + int(last_commission) + int(last_personal_commission)
    this_total = int(staff.basic_salary) + int(this_commission) + int(this_personal_commission)


    context={
        'staff' : staff,
        'members' : members,
        'today_members' : today_members,
        'today_members_pay' : today_members_pay,
        'thisweek_members' : thisweek_members,
        'thisweek_members_pay' :thisweek_members_pay,
        'thismonth_members' : thismonth_members,
        'thismonth_members_pay_before' : thismonth_members_pay_before,
        'lastmonth_members_pay' : lastmonth_members_pay,
        #커미션#
        'basic_salary' : basic_salary,
        'last_team_sales_before' : last_team_sales_before,
        'last_commission_rate' : last_commission_rate,
        'last_commission' : last_commission,
        'last_total' : last_total,
        #이번달 커미션#
        'this_team_sales_before' : this_team_sales_before,
        'this_team_sales' : this_team_sales,
        'this_commission_rate': this_commission_rate,
        'this_commission' : this_commission,
        'this_total' : this_total,
        #팀원 개인수당
        'last_personal_commission_rate':last_personal_commission_rate,
        'last_personal_commission' : last_personal_commission,
        'this_personal_commission_rate' : this_personal_commission_rate,
        'this_personal_commission' : this_personal_commission,
        ###환불
        'this_refund_list' : this_refund_list,
        'last_personal_refund' : last_personal_refund,
        'last_FC_refund' : last_FC_refund,
        'last_FC_refund_amount' : last_FC_refund_amount,
        'this_personal_refund' : this_personal_refund,
        'this_FC_refund' : this_FC_refund,
        'this_FC_refund_amount' : this_FC_refund_amount,
    }
    return render(request, 'mypage.html', context)

def PT_mypage(request, staff_id): #피트니스의 마이페이지
    staff = User.objects.get(id=staff_id)
    PT_members = staff.PT_members.all()
    date = datetime.date.today() #오늘 받기
    #####오늘#####
    today_members = PT_members.filter(PT_registered_date=date) #오늘 등록한 회원
    today_members_pay = today_members.aggregate(Sum('PT_payment_amount')).get('PT_payment_amount__sum',0.00)
    #####이번주####
    start_week = date- datetime.timedelta(date.weekday()) #이번주(월요일시작)
    end_week = start_week + datetime.timedelta(6) #월요일 + 6 (일요일)
    this_month = datetime.timedelta(date.month)
    thisweek_members = PT_members.filter(PT_registered_date__range=[start_week, end_week])
    thisweek_members_pay = thisweek_members.aggregate(Sum('PT_payment_amount')).get('PT_payment_amount__sum',0.00)
    ####이번달####
    this_month_start = datetime.datetime(date.year, date.month, 1) #이번달의 1일
    thismonth_members = PT_members.filter(PT_registered_date__range=[this_month_start, date])
    thismonth_members_pay = thismonth_members.aggregate(Sum('PT_payment_amount')).get('PT_payment_amount__sum',0.00) if thismonth_members else 0

    ###저번달
    if date.month == 1: #1월이면, 작년 12월 return
        year = date.year-1
        last_month= 12
    else:
        year = date.year
        last_month = date.month-1

    lastmonth_members = PT_members.filter(PT_registered_date__year=year).filter(PT_registered_date__month=last_month)
    lastmonth_members_pay = lastmonth_members.aggregate(Sum('PT_payment_amount')).get('PT_payment_amount__sum',0.00) if lastmonth_members else 0
    #####커미션##########
    basic_salary = staff.basic_salary
    last_team_sales_before=int(0)
    last_tuition = int(0)
    this_team_sales_before=int(0)
    this_tuition = int(0)

    team_members = User.objects.filter(groups__name='Fitness') #피트니스 팀 직원들
    lastmonth_schedules = Schedule.objects.filter(Trainer=staff).filter(start__year=year).filter(start__month=last_month).filter(~Q(title__icontains='SV')).filter(~Q(title__icontains='OT')) #지난달에 pt받은 회원들
    thismonth_schedules = Schedule.objects.filter(Trainer=staff).filter(start__year=date.year).filter(start__month=date.month).filter(~Q(title__icontains='SV')).filter(~Q(title__icontains='OT')) #이번달에 pt받은 회원들

    for f in team_members:
        PT_members = f.PT_members.all()
        last_members = PT_members.filter(PT_registered_date__year=year).filter(PT_registered_date__month=last_month) #지난달 등록한 Fitness PT회원들
        members_pay = last_members.aggregate(Sum('PT_payment_amount')).get('PT_payment_amount__sum',0.00) if last_members else 0 #Suspect some of members is None
        last_team_sales_before = last_team_sales_before + members_pay #저번달 팀 총 매출
        this_members = PT_members.filter(PT_registered_date__year=year).filter(PT_registered_date__month=date.month) #이번달 등록한 Fitness PT회원들
        this_members_pay = this_members.aggregate(Sum('PT_payment_amount')).get('PT_payment_amount__sum',0.00) if this_members else 0 #Suspect some of members is None
        this_team_sales_before = this_team_sales_before + this_members_pay # 이번달 팀 총 매출


    ######################환불################

    last_refund_list = RefundHistory.objects.none()
    this_refund_list = RefundHistory.objects.none()
    for m in staff.PT_members.all(): #나의 회원만.
        payment = m.PaymentHistory.filter(division="Fitness")
        for p in payment:
            try:
                last_refund = RefundHistory.objects.filter(payment=p).filter(refund_date__year=year).filter(refund_date__month=last_month)
                last_refund_list |= last_refund

                this_refund = RefundHistory.objects.filter(payment=p).filter(refund_date__range=[this_month_start, date])
                this_refund_list |= this_refund
            except:
                pass
    last_refund_list = last_refund_list.distinct()
    this_refund_list = this_refund_list.distinct()

    last_personal_refund = int(0)
    for i in last_refund_list:
        last_personal_refund = last_personal_refund + i.refund_amount #지난달 나의 회원 총 환불.

    this_personal_refund = int(0)
    for i in this_refund_list:
        this_personal_refund = this_personal_refund + i.refund_amount #이번달 나의 회원 총 환불.

    last_Fitness_refund = RefundHistory.objects.filter(division="Fitness").filter(refund_date__year=year).filter(refund_date__month=last_month)  #지난달 회원권 총 환불.

    last_Fitness_refund_amount = last_Fitness_refund.aggregate(Sum('refund_amount')).get('refund_amount__sum',0.00) if last_Fitness_refund else 0 #Suspect some of members

    this_Fitness_refund = RefundHistory.objects.filter(division="Fitness").filter(refund_date__range=[this_month_start, date]) #이번달 회원권 총 환불.

    this_Fitness_refund_amount = this_Fitness_refund.aggregate(Sum('refund_amount')).get('refund_amount__sum',0.00) if this_Fitness_refund else 0 #Suspect some of members

    #######환불End####################
    #
    ######총매출 - 환불##############
    #지난달
    last_team_sales = last_team_sales_before - last_Fitness_refund_amount
    if last_team_sales <0:
        last_team_sales=0

    lastmonth_members_pay_before = lastmonth_members_pay
    lastmonth_members_pay = lastmonth_members_pay_before - last_personal_refund
    if lastmonth_members_pay < 0:
        lastmonth_members_pay=0

    ## 이번달 FC팀 총 매출 - 이번달 FC팀 환불
    this_team_sales = this_team_sales_before - this_Fitness_refund_amount
    if this_team_sales < 0 :
        this_team_sales =0

    # 이번달 나의 총 매출 - 이번달 나의 환불
    thismonth_members_pay_before = thismonth_members_pay
    thismonth_members_pay = thismonth_members_pay_before - this_personal_refund
    if thismonth_members_pay < 0:
        thismonth_members_pay = 0

    ######총매출 - 환불 End###########
    #

    #팀장이면
    if staff.teamleader == True:
        last_commissions = Fitness_Teamledaer_Commission.objects.filter(min_sales__lte=last_team_sales).filter(max_sales__gt=last_team_sales)
        this_commissions = Fitness_Teamledaer_Commission.objects.filter(min_sales__lte=this_team_sales).filter(max_sales__gt=this_team_sales)

    #팀원이면
    else:
        last_commissions = Fitness_Personal_Commission.objects.filter(min_personal_sales__lte=lastmonth_members_pay).filter(max_personal_sales__gt=lastmonth_members_pay)
        this_commissions = Fitness_Personal_Commission.objects.filter(min_personal_sales__lte=thismonth_members_pay).filter(max_personal_sales__gt=thismonth_members_pay)


    for c in last_commissions:
        last_commission_rate = c.commission
        last_tuition_commission = c.tuition_commission

    last_commission = float(last_team_sales) * last_commission_rate/100

    for c in this_commissions:
        this_commission_rate = c.commission
        this_tuition_commission = c.tuition_commission

    this_commission = float(this_team_sales) * this_commission_rate/100

    for s in lastmonth_schedules:
        last_personal_tuition = s.unitprice * last_tuition_commission/100
        last_tuition = last_tuition + last_personal_tuition

    for s in thismonth_schedules:
        this_personal_tuition = s.unitprice * this_tuition_commission/100
        this_tuition = this_tuition + this_personal_tuition

    last_total = int(staff.basic_salary) + int(last_commission) + int(last_tuition)
    this_total = int(staff.basic_salary) + int(this_commission) + int(this_tuition)

    context={
        'staff' : staff,
        'PT_members' : PT_members,
        'today_members' : today_members,
        'today_members_pay' : today_members_pay,
        'thisweek_members' : thisweek_members,
        'thisweek_members_pay' :thisweek_members_pay,
        'thismonth_members' : thismonth_members,
        'thismonth_members_pay' : thismonth_members_pay,
        'thismonth_members_pay_before':thismonth_members_pay_before,
        'basic_salary' :basic_salary,
        'lastmonth_schedules' :lastmonth_schedules,
        'thismonth_schedules':thismonth_schedules,

        'lastmonth_members_pay' :lastmonth_members_pay,
        #지난달
        'last_team_sales_before' : last_team_sales_before,
        'last_commission_rate' : last_commission_rate,
        'last_commission' : last_commission,
        'last_tuition_commission' : last_tuition_commission,
        'last_tuition' : last_tuition,
        'last_total' : last_total,
        #이번달
        'this_team_sales_before' : this_team_sales_before,
        'this_commission_rate' : this_commission_rate,
        'this_commission' : this_commission,
        'this_tuition_commission' : this_tuition_commission,
        'this_tuition' : this_tuition,
        'this_total' : this_total,
        ###환불
        'this_refund_list' : this_refund_list,
        'last_personal_refund' : last_personal_refund,
        'last_Fitness_refund' : last_Fitness_refund,
        'last_Fitness_refund_amount' : last_Fitness_refund_amount,
        'this_personal_refund' : this_personal_refund,
        'this_Fitness_refund' : this_Fitness_refund,
        'this_Fitness_refund_amount' : this_Fitness_refund_amount,

    }

    return render(request, 'PT_mypage.html', context)

def Pilates_mypage(request, staff_id):
    staff = User.objects.get(id=staff_id)
    Pil_members = staff.Pil_members.all()
    date = datetime.date.today() #오늘 받기
    #####오늘#####
    today_members = Pil_members.filter(Pil_registered_date=date) #오늘 등록한 회원
    today_members_pay = today_members.aggregate(Sum('Pil_payment_amount')).get('Pil_payment_amount__sum',0.00)
    #####이번주####
    start_week = date- datetime.timedelta(date.weekday()) #이번주(월요일시작)
    end_week = start_week + datetime.timedelta(6) #월요일 + 6 (일요일)
    this_month = datetime.timedelta(date.month)
    thisweek_members = Pil_members.filter(Pil_registered_date__range=[start_week, end_week])
    thisweek_members_pay = thisweek_members.aggregate(Sum('Pil_payment_amount')).get('Pil_payment_amount__sum',0.00)
    ####이번달####
    this_month_start = datetime.datetime(date.year, date.month, 1) #이번달의 1일
    thismonth_members = Pil_members.filter(Pil_registered_date__range=[this_month_start, date])
    thismonth_members_pay = thismonth_members.aggregate(Sum('Pil_payment_amount')).get('Pil_payment_amount__sum',0.00) if thismonth_members else 0

    ###저번달
    if date.month == 1: #1월이면, 작년 12월 return
        year = date.year-1
        last_month= 12
    else:
        year = date.year
        last_month = date.month-1

    lastmonth_members = Pil_members.filter(Pil_registered_date__year=year).filter(Pil_registered_date__month=last_month)
    lastmonth_members_pay = lastmonth_members.aggregate(Sum('Pil_payment_amount')).get('Pil_payment_amount__sum',0.00) if lastmonth_members else 0
    #####커미션##########
    basic_salary = staff.basic_salary
    last_team_sales_before=int(0)
    last_tuition = int(0)
    this_team_sales_before=int(0)
    this_tuition = int(0)

    team_members = User.objects.filter(groups__name='Pilates') #필라테스 팀 직원들
    lastmonth_PT_schedules = Schedule.objects.filter(Trainer=staff).filter(start__year=year).filter(start__month=last_month).filter(GX=False).filter(~Q(title__icontains='SV')).filter(~Q(title__icontains='OT')) #지난달에 pt받은 회원들
    thismonth_PT_schedules = Schedule.objects.filter(Trainer=staff).filter(start__year=date.year).filter(start__month=date.month).filter(GX=False).filter(~Q(title__icontains='SV')).filter(~Q(title__icontains='OT')) #이번달에 pt받은 회원들

    lastmonth_GX_schedules = Schedule.objects.filter(Trainer=staff).filter(start__year=year).filter(start__month=last_month).filter(GX=True) #지난달 GX 갯수
    thismonth_GX_schedules = Schedule.objects.filter(Trainer=staff).filter(start__year=date.year).filter(start__month=date.month).filter(GX=True) #이번달 GX 갯수

    for f in team_members:
        Pil_members = f.Pil_members.all()
        last_members = Pil_members.filter(Pil_registered_date__year=year).filter(Pil_registered_date__month=last_month) #지난달 등록한 Pilates PT회원들
        last_members_pay = last_members.aggregate(Sum('Pil_payment_amount')).get('Pil_payment_amount__sum',0.00) if last_members else 0 #Suspect some of members is None
        last_team_sales_before = last_team_sales_before + last_members_pay #저번달 팀 총 매출
        this_members = Pil_members.filter(Pil_registered_date__year=year).filter(Pil_registered_date__month=date.month) #이번달 등록한 Pilates PT회원들
        this_members_pay = this_members.aggregate(Sum('Pil_payment_amount')).get('Pil_payment_amount__sum',0.00) if this_members else 0 #Suspect some of members is None
        this_team_sales_before = this_team_sales_before + this_members_pay # 이번달 팀 총 매출

    ######################환불################

    last_refund_list = RefundHistory.objects.none()
    this_refund_list = RefundHistory.objects.none()
    for m in staff.Pil_members.all(): #나의 회원만.
        payment = m.PaymentHistory.filter(division="Pilates")
        for p in payment:
            try:
                last_refund = RefundHistory.objects.filter(payment=p).filter(refund_date__year=year).filter(refund_date__month=last_month)
                last_refund_list |= last_refund

                this_refund = RefundHistory.objects.filter(payment=p).filter(refund_date__range=[this_month_start, date])
                this_refund_list |= this_refund
            except:
                pass
    last_refund_list = last_refund_list.distinct()
    this_refund_list = this_refund_list.distinct()

    last_personal_refund = int(0)
    for i in last_refund_list:
        last_personal_refund = last_personal_refund + i.refund_amount #지난달 나의 회원 총 환불.

    this_personal_refund = int(0)
    for i in this_refund_list:
        this_personal_refund = this_personal_refund + i.refund_amount #이번달 나의 회원 총 환불.

    last_Pilates_refund = RefundHistory.objects.filter(division="Pilates").filter(refund_date__year=year).filter(refund_date__month=last_month)  #지난달 필라팀 총 환불.

    last_Pilates_refund_amount = last_Pilates_refund.aggregate(Sum('refund_amount')).get('refund_amount__sum',0.00) if last_Pilates_refund else 0 #Suspect some of members

    this_Pilates_refund = RefundHistory.objects.filter(division="Pilates").filter(refund_date__range=[this_month_start, date]) #이번달 필라팀 총 환불.

    this_Pilates_refund_amount = this_Pilates_refund.aggregate(Sum('refund_amount')).get('refund_amount__sum',0.00) if this_Pilates_refund else 0 #Suspect some of members

    #######환불End####################
    #
    ######총매출 - 환불##############
    #지난달
    last_team_sales = last_team_sales_before - last_Pilates_refund_amount
    if last_team_sales <0:
        last_team_sales=0

    lastmonth_members_pay_before = lastmonth_members_pay
    lastmonth_members_pay = lastmonth_members_pay_before - last_personal_refund
    if lastmonth_members_pay < 0:
        lastmonth_members_pay=0

    ## 이번달 FC팀 총 매출 - 이번달 FC팀 환불
    this_team_sales = this_team_sales_before - this_Pilates_refund_amount
    if this_team_sales < 0 :
        this_team_sales =0

    # 이번달 나의 총 매출 - 이번달 나의 환불
    thismonth_members_pay_before = thismonth_members_pay
    thismonth_members_pay = thismonth_members_pay_before - this_personal_refund
    if thismonth_members_pay < 0:
        thismonth_members_pay = 0

    ######총매출 - 환불 End###########
    #
    #

    #팀장이면
    if staff.teamleader == True:
        last_PT_commission_rate = 0
        this_PT_commission_rate = 0 #팀장은 PT비율로 안하니 0으로.
        last_commissions = Pilates_Teamleader_Commission.objects.filter(min_sales__lte=last_team_sales).filter(max_sales__gt=last_team_sales)
        this_commissions = Pilates_Teamleader_Commission.objects.filter(min_sales__lte=this_team_sales).filter(max_sales__gt=this_team_sales)

        for c in last_commissions:
            last_commission_rate = c.commission
            last_GX_tuition = c.GX_tuition
            last_PT_tuition = c.PT_tuition

        for c in this_commissions:
            this_commission_rate = c.commission
            this_GX_tuition = c.GX_tuition
            this_PT_tuition = c.PT_tuition

        last_commission = float(last_team_sales) * last_commission_rate/100
        this_commission = float(this_team_sales) * this_commission_rate/100

        last_GX_commission = lastmonth_GX_schedules.count() * last_GX_tuition
        last_PT_commission = lastmonth_PT_schedules.count() * last_PT_tuition

        this_GX_commission = thismonth_GX_schedules.count() * this_GX_tuition
        this_PT_commission = thismonth_PT_schedules.count() * this_PT_tuition


    #팀원이면
    else:
        last_commission = int(0)
        this_commission = int(0) #팀원은, 팀커미션 없으니 0으로.
        last_commission_rate = 0
        this_commission_rate = 0
        if staff.pilates_GX == 'basic': #고정된 GX수업비
            for gx in Pilates_GX_Basic.objects.all(): #2만원인 gx 커미션정책 가져오기.
                last_GX_commission = gx.tuition * lastmonth_GX_schedules.count()
                this_GX_commission = gx.tuition * thismonth_GX_schedules.count()


        else: #명수에 따른 GX수업비
            last_GX_commission = int(0)
            this_GX_commission = int(0)
            for gx in Pilates_GX_DependingNum.objects.all():
                min_num = gx.depending_number_min #1, 3, 5
                max_num = gx.depending_number_max #2, 4, 7

                last_GX = lastmonth_GX_schedules.filter(number__lte=max_num).filter(number__gte=min_num) #처음엔 1~2명, 다음엔 3~4명, 다음엔 5~6명

                last_GX_commission = last_GX_commission + (last_GX.count() * gx.tuition)

                this_GX = thismonth_GX_schedules.filter(number__lte=max_num).filter(number__gte=min_num) #처음엔 1~2명, 다음엔 3~4명, 다음엔 5~6명
                this_GX_commission +=  (this_GX.count() * gx.tuition)

        if staff.pilates_PT == 'basic': #매출에 따른 PT수업료.
            last_commissions = Pilates_Commission.objects.filter(min_personal_sales__lte=lastmonth_members_pay).filter(max_personal_sales__gt=lastmonth_members_pay)
            this_commissions = Pilates_Commission.objects.filter(min_personal_sales__lte=thismonth_members_pay).filter(max_personal_sales__gt=thismonth_members_pay)

            for c in last_commissions:
                last_PT_commission_rate = c.tuition_commission

            last_PT_commission = lastmonth_PT_schedules.count() * last_PT_commission_rate/100

            for c in this_commissions:
                this_PT_commission_rate = c.tuition_commission

            this_PT_commission = thismonth_PT_schedules.count() * this_PT_commission_rate/100

        else: #고정된 PT수업료 비율
            for pt in Pilates_PT.objects.all():
                last_PT_commission_rate = pt.fix_rate
                this_PT_commission_rate = pt.fix_rate

            last_PT_commission = float(lastmonth_members_pay) * last_PT_commission_rate/100
            this_PT_commission = float(thismonth_members_pay) * this_PT_commission_rate/100

    last_total = int(staff.basic_salary) + int(last_commission) + int(last_GX_commission) + int(last_PT_commission)
    this_total = int(staff.basic_salary) + int(this_commission) + int(this_GX_commission) + int(this_PT_commission)

    context={
        'staff' : staff,
        'Pil_members' : Pil_members,
        'today_members' : today_members,
        'today_members_pay' : today_members_pay,
        'thisweek_members' : thisweek_members,
        'thisweek_members_pay' :thisweek_members_pay,
        'thismonth_members' : thismonth_members,
        'thismonth_members_pay' : thismonth_members_pay,
        'thismonth_members_pay_before':thismonth_members_pay_before,
        'basic_salary' :basic_salary,

        'lastmonth_members_pay' :lastmonth_members_pay,
        #지난달
        'last_team_sales_before' : last_team_sales_before,
        'last_commission' : last_commission,
        'last_commission_rate' : last_commission_rate,
        'last_GX_commission' : last_GX_commission,
        'last_PT_commission' : last_PT_commission,
        'lastmonth_GX_schedules' : lastmonth_GX_schedules.count(),
        'lastmonth_PT_schedules' : lastmonth_PT_schedules.count(),
        'last_PT_commission_rate' : last_PT_commission_rate,
        'last_total' : last_total,
        #이번달
        'this_team_sales_before' : this_team_sales_before,
        'this_commission' : this_commission,
        'this_commission_rate' : this_commission_rate,
        'this_GX_commission' : this_GX_commission,
        'this_PT_commission' : this_PT_commission,
        'thismonth_GX_schedules' :thismonth_GX_schedules.count(),
        'thismonth_PT_schedules' : thismonth_PT_schedules.count(),
        'this_PT_commission_rate' : this_PT_commission_rate,
        'this_total' : this_total,
        ###환불
        'this_refund_list' : this_refund_list,
        'last_personal_refund' : last_personal_refund,
        'last_Pilates_refund' : last_Pilates_refund,
        'last_Pilates_refund_amount' : last_Pilates_refund_amount,
        'this_personal_refund' : this_personal_refund,
        'this_Pilates_refund' : this_Pilates_refund,
        'this_Pilates_refund_amount' : this_Pilates_refund_amount,

    }
    return render(request, 'Pilates_mypage.html', context)

def schedule(request): #스케줄 관리 페이지
    schedules = request.user.schedule.filter(~Q(title__icontains='OT')) #OT를 제외한 나의 스케줄
    OT_schedules = request.user.schedule.filter(title__icontains='OT') #OT 스케줄
    PT_members = request.user.PT_members.all() #나의 PT 회원들
    Pil_members = request.user.Pil_members.all()
    date = datetime.date.today() #오늘 받기
    context = {
        'PT_members' : PT_members,
        'Pil_members':Pil_members,
        'date' : date,
        'schedules' : schedules,
        'OT_schedules' : OT_schedules,
    }
    return render(request, 'schedule.html', context)

def PT_member_detail(request, PT_member_id):
    PT_member = Member.objects.get(id=PT_member_id)
    schedules = Schedule.objects.filter(name=PT_member).filter(birth=PT_member.birth)
    member_history = History.objects.filter(user=PT_member).filter(birth=PT_member.birth) #이름과 생일 모두 일치하는 회원 기록만 불러오기
    member_pil_history = Pil_History.objects.filter(user=PT_member).filter(birth=PT_member.birth) #이름과 생일 모두 일치하는 회원 기록만 불러오기

    context = {
        'PT_member' : PT_member,
        'schedules' : schedules,
        'member_history' : member_history,
        'member_pil_history' : member_pil_history,
    }
    return render(request, 'PT_member_detail.html', context)

def PT_member_session_end(request, PT_member_id):
    p = Member.objects.get(id=PT_member_id)
    if p.re_registered==True: #재등록회원이라면
        for h in History.objects.filter(user=p).filter(birth=p.birth).filter(PT_registered_date__gte=p.PT_registered_date): #큰쪽이 더 최신날짜
        #해당회원의 히스토리중, 만료된 세션 등록일보다 더 최근에 등록한 히스토리를 찾는다.
            p.Trainer = h.Trainer
            p.registered_session = h.registered_session
            p.PT_payment_amount = h.PT_payment_amount
            p.PT_payment_method = h.PT_payment_method
            p.unitprice = h.unitprice
            p.period_PT = h.period_PT
            p.PT_registered_date = h.PT_registered_date
            p.used_session = 0
            p.re_registered = False #재등록여부는 다시 false로
            p.PT_status = 0 #만료
            p.save()
    else: #재등록회원이 아니라면, pt등록정보 초기화
        p.Trainer = None
        p.registered_session = None
        p.PT_payment_amount = None
        p.PT_payment_method = None
        p.unitprice = None
        p.period_PT = None
        p.PT_registered_date = None
        p.used_session = 0
        p.save()
    return redirect('schedule')

def PT_member_delete(request, PT_member_id):
    # member = Member.objects.get(id=PT_member_id)
    for p in request.user.PT_members.filter(id=PT_member_id):
        #PT_register할때 했던 것들 다 null로 바꾸기
        p.Trainer = None
        # p.registered_session = None
        # p.PT_payment_amount = None
        # p.PT_payment_method = None
        # p.unitprice = None
        # p.period_PT = None
        # p.PT_registered_date = None
        # p.re_registered = False
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
    staff = request.user
    member = Member.objects.get(id=member_id)
    member.PT_status = 1
    member.save()

    if request.method == 'POST':
        form = PT_RegisterForm(request.POST , instance=member)
        form1 = PT_Register_HistoryForm(request.POST or None)
        if form.is_valid() and form1.is_valid():
            if member.Trainer != request.user: #재등록이 아니라면,
                member.Trainer = request.user
                member.PT_registered_date = datetime.date.today() #오늘
                form.save()

            else: #재등록이라면 재등록여부를 true로 하기
                Member.objects.filter(id=member_id).update(re_registered=True)
                # 기본 멤버정보는 안바뀌고 PT 등록(history) 기록만 남기기

            history = form1.save(commit=False)
            history.user = member
            history.birth = member.birth
            history.Trainer=request.user
            history.division = "Fitness"
            history.PT_registered_date = datetime.date.today() #오늘


            check = History.objects.filter(user=member).filter(birth=member.birth) #그동안 몇번 pt등록했는지 확인
            if check.exists():
                history_num = check.count()
                history.Num = history_num + 1
            else:
                history.Num = 1

            history.save() #PT내역.

            PaymentHistory.objects.create( #결제내역
                user = member,
                division = 'Fitness',
                date = member.PT_registered_date,
                start_date = member.start_date,
                end_date = member.end_date,
                registered_session = member.registered_session,
                payment_amount = member.PT_payment_amount,
            )

            return redirect('schedule')


    else: #POST요청이 아니라면
        form=PT_RegisterForm()
        form1 = PT_Register_HistoryForm()

    return render(request, 'PT_register_create.html',{
        'member' : member,
        'form':form,
        'form1':form1,
        })

def Pil_register_create(request, member_id):
    staff = request.user
    member = Member.objects.get(id=member_id)
    member.Pil_status = 1
    member.save()

    if request.method == 'POST':
        form = Pil_RegisterForm(request.POST , instance=member)
        form1 = Pil_Register_HistoryForm(request.POST or None)
        if form.is_valid() and form1.is_valid():
            if member.Pil_Trainer != request.user: #재등록이 아니라면,
                member.Pil_Trainer = request.user
                member.Pil_registered_date = datetime.date.today() #오늘
                form.save()

            else: #재등록이라면 재등록여부를 true로 하기
                Member.objects.filter(id=member_id).update(Pil_re_registered=True)
                # 기본 멤버정보는 안바뀌고 PT 등록(history) 기록만 남기기

            history = form1.save(commit=False)
            history.user = member
            history.birth = member.birth
            history.Pil_Trainer=request.user
            history.division = "Pilates"
            history.Pil_registered_date = datetime.date.today() #오늘


            check = Pil_History.objects.filter(user=member).filter(birth=member.birth) #그동안 몇번 pt등록했는지 확인
            if check.exists():
                history_num = check.count()
                history.Num = history_num + 1
            else:
                history.Num = 1

            history.save() #PT내역.

            PaymentHistory.objects.create( #결제내역
                user = member,
                division = 'Pilates',
                date = datetime.date.today(), #오늘,
                start_date = member.start_date,
                end_date = member.end_date,
                registered_session = member.Pil_registered_session,
                payment_amount = member.Pil_payment_amount,
            )

            return redirect('schedule')


    else: #POST요청이 아니라면
        form=Pil_RegisterForm()
        form1 = Pil_Register_HistoryForm()

    return render(request, 'Pil_register_create.html',{
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

def OT_schedule_add(request):
    if request.is_ajax():
        start_original = request.POST.get('start',None)
        s1 = start_original.split()[1:5] #korean standard time을 datetimefield 형식에 맞추기 위해 split ['Jul', '06','2017','08:00:00']
        s = ' '.join(s1) #split후 다시 합치기
        start= datetime.datetime.strptime(s, '%b %d %Y %H:%M:%S') #%T = %H:%M:%S
        end = datetime.datetime.strptime(s, '%b %d %Y %H:%M:%S')
        title = request.POST.get('title',None)
        member = Member.objects.get(id=request.POST.get('id')) #넘겨온 id의 회원 찾기

        member.OT_used_session = member.OT_used_session + 1
        member.save()

        Schedule.objects.create(
                Trainer = request.user,
                name=member,
                birth= member.birth,
                title = title,
                OT_used_session = member.OT_used_session,
                start = start,
                end = end
                )
        context={}
        return HttpResponse(json.dumps(context), content_type='application/json')


def schedule_add(request):
    if request.is_ajax():
        start_original = request.POST.get('start',None)
        s1 = start_original.split()[1:5] #korean standard time을 datetimefield 형식에 맞추기 위해 split ['Jul', '06','2017','08:00:00']
        s = ' '.join(s1) #split후 다시 합치기
        start= datetime.datetime.strptime(s, '%b %d %Y %H:%M:%S') #%T = %H:%M:%S
        end = datetime.datetime.strptime(s, '%b %d %Y %H:%M:%S')

        title = request.POST.get('title',None)
        if 'GX' in title: # GX추가라면,
            number = request.POST.get('number',None)
            Schedule.objects.create(
                Trainer = request.user,
                title = title,
                start = start,
                end = end,
                GX = True,
                number = number
                )
            context={}

        else:
            member = Member.objects.get(id=request.POST.get('id')) #넘겨온 id의 회원 찾기

            succeeding_schedule = Schedule.objects.filter(name=member).filter(birth=member.birth).filter(PT_registered_date=member.PT_registered_date).filter(start__gt=start).filter(~Q(title__icontains='SV')) #뒤에 있는 스케줄들

            if 'SV' in title: #OT 버튼이라면
                member.used_session = member.used_session+0 #세션추가 없음
                unitprice= 0
                used_session = member.used_session
            else:
                if succeeding_schedule.exists(): #현재 추가하는 스케줄보다 뒤에 스케줄이 있다면
                    first_succeeding_schedule = succeeding_schedule.latest('start') # 뒤에있는 것중, 가장 최근
                    used_session = first_succeeding_schedule.used_session  # 현재 추가하는 스케줄의 사용된세션 = 가장 최근세션의 사용된세션

                    for s in succeeding_schedule.order_by('start'): #시간에 따른 오림차순
                        s.used_session = s.used_session + 1 #빠른세션들 사용된세션을 +1
                        s.save()

                    member.used_session = member.used_session+1 #사용된 세션1회추가
                    unitprice = member.PT_unitprice

                    member.save() # +1 상태 저장

                else:  # 뒤에 스케줄이 없다면
                    member.used_session = member.used_session+1 #사용된 세션1회추가
                    unitprice = member.PT_unitprice

                    member.save() # +1 상태 저장

                    used_session = member.used_session

            Schedule.objects.create(
                Trainer=request.user,
                name = member,
                title = title, #받아온 data중 title 얻기
                start = start,
                end = end,
                birth= member.birth,
                PT_registered_date = member.PT_registered_date,
                used_session = used_session,
                registered_session = member.registered_session,
                unitprice = unitprice #수수료 10%제외한 단가
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
    print(schedule_id)
    schedule = Schedule.objects.get(id=schedule_id) #해당 스케줄찾기
    member = schedule.name #해당 회원찾기
    if schedule.title == "GX":
        pass
    elif 'SV' in schedule.title:
        member.used_session = member.used_session+0 #세션삭제 없음

    elif 'OT' in schedule.title:
        member.OT_used_session = member.OT_used_session - 1
        pass
        # member.OT_used_session = member.OT_used_session - 1
        # member.save()

    else: #정식 PT

        succeeding_schedule = Schedule.objects.filter(name=member).filter(birth=member.birth).filter(PT_registered_date=schedule.PT_registered_date).filter(start__gt=schedule.start).filter(~Q(title__icontains='SV')) #같은 회원권 스케줄중(OT가 아닌), 빠른 날짜가 있는지 찾는다. 큰쪽이 더 최신날짜

        if succeeding_schedule.exists(): #현재 지우는 스케줄보다 뒤에 스케줄이 있다면
            for s in succeeding_schedule.order_by('start'): #시간에 따른 오림차순
                s.used_session = s.used_session - 1 #빠른세션들 사용된세션
                s.save()
        else:
            pass

        member.used_session = member.used_session-1
            #스케줄 삭제시 세션 횟수도 하나 삭제.
    member.save() # +0 or -1 상태 저장한

    schedule.delete() #스케줄 삭제

    return redirect('schedule')

def purchasing_application(request):
    return render(request, 'purchasing_application.html')