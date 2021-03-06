from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Sum, Q
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from management.models import FC_Teamleader_Commission, FC_Personal_Commission, FC_Team_Commission, Fitness_Teamledaer_Commission, Fitness_Personal_Commission, Pilates_Teamleader_Commission,  Pilates_Commission, Pilates_GX_Basic, Pilates_GX_DependingNum, Pilates_PT
from authentication.models import User,FC_Salary, Fitness_Salary,Pilates_Salary
from staff.models import Member,PaymentHistory, RefundHistory, Schedule
from management.forms import *
from decimal import Decimal
import datetime
import json
from collections import OrderedDict

# Create your views here.

def member_management(request):
    order_by = request.GET.get('order_by', 'name')
    staff_order_by = request.GET.get('staff_order_by', 'groups')
    member_list = Member.objects.all().order_by(order_by)
    staff_list = User.objects.all().order_by(staff_order_by)
    context = {
        'staff_list':staff_list,
        'member_list' : member_list,
    }
    return render(request, 'management/member_management.html', context)

def member_search(request):

    keyword = request.GET.get('q','') #검색 키워드
    condition=(Q(name__icontains=keyword) | Q(phone_num__icontains=keyword))
    search_member = Member.objects.filter(condition)#검색 조건 이름, 휴대번호

    staff_order_by = request.GET.get('staff_order_by', 'groups')
    staff_list = User.objects.all().order_by(staff_order_by)
    context= {
        'staff_list' : staff_list,
        'member_list' : search_member,
        'q' : keyword,
    }
    return render(request, 'management/member_management.html', context)

def payment_history(request, member_id):
    member = Member.objects.get(id=member_id)
    paymenthistory = PaymentHistory.objects.filter(user=member)
    active_paymenthistory = PaymentHistory.objects.filter(user=member).filter(status=1)
    refund_paymenthistory = PaymentHistory.objects.filter(user=member).filter(status=2)
    expirated_paymenthistory = PaymentHistory.objects.filter(user=member).filter(status=0)

    context = {
        'member' : member,
        'paymenthistory' : paymenthistory,
        'active_paymenthistory' : active_paymenthistory,
        'refund_paymenthistory' : refund_paymenthistory,
        'expirated_paymenthistory' : expirated_paymenthistory,
    }
    return render(request, 'management/payment_history.html', context)

def refund(request, history_id):
    payment_history = PaymentHistory.objects.get(id=history_id)
    member = payment_history.user
    payment_history.status = 2
    payment_history.save()
    today = datetime.date.today()

    period = (payment_history.end_date - payment_history.start_date).days #총 이용 기간
    remaining_period = (payment_history.end_date - today).days/(payment_history.end_date - payment_history.start_date).days #남은 기간
    used_period = (today - payment_history.start_date).days  #사용한 일 수

    oneday_cost = payment_history.payment_amount / Decimal(period) # 하루이용료 = 전체금액/이용기간

    fees = payment_history.payment_amount * Decimal(0.1) #위약금10%
    used_amount = oneday_cost * Decimal(used_period) # 이용료 = 하루이용료 * 사용한 기간

    if payment_history.division == "Membership":
        member.Membership_status = 2
        member.save()

        total_utility_cost = fees + used_amount

        refund_amount = payment_history.payment_amount - total_utility_cost

        RefundHistory.objects.create(
            payment = payment_history,
            division = "Membership",
            date = payment_history.date,
            refund_date = today, #오늘
            fees = fees,
            oneday_cost = oneday_cost,
            used_period = used_period,
            used_amount = used_amount,
            total_utility_cost = total_utility_cost,
            refund_amount = refund_amount
        )

    elif payment_history.division =='Fitness':
        member.PT_status = 2
        member.save()
        remaining_session = (payment_history.registered_session - member.used_session )/payment_history.registered_session
        used_session= member.used_session /payment_history.registered_session

        fees = payment_history.payment_amount * Decimal(0.1) #위약금10%
        used_amount =  payment_history.payment_amount * Decimal(0.9) * Decimal(used_session) #이용료
        total_utility_cost = fees + used_amount

        #환급액 = 전체 금액 - 위약금-이용료
        refund_amount = payment_history.payment_amount - total_utility_cost

        RefundHistory.objects.create(
            payment = payment_history,
            division = "Fitness",
            date = payment_history.date,
            refund_date = today, #오늘
            fees = fees,
            used_amount = used_amount,
            total_utility_cost = total_utility_cost,
            refund_amount = refund_amount
        )
    elif payment_history.division =='Pilates':
        member.Pil_status = 2
        member.save()
        remaining_session = (payment_history.registered_session - member.used_session )/payment_history.registered_session
        used_session= member.Pil_used_session /payment_history.registered_session

        fees = payment_history.payment_amount * Decimal(0.1) #위약금10%
        used_amount =  payment_history.payment_amount * Decimal(0.9) * Decimal(used_session) #이용료
        total_utility_cost = fees + used_amount

        refund_amount = payment_history.payment_amount - total_utility_cost

        RefundHistory.objects.create(
            payment = payment_history,
            division = "Pilates",
            date = payment_history.date,
            refund_date = today, #오늘
            fees = fees,
            used_amount = used_amount,
            total_utility_cost = total_utility_cost,
            refund_amount = refund_amount
        )
    elif payment_history.division == 'H_Locker':
        member.H_locker = None
        member.save()

        total_utility_cost = fees + used_amount
        refund_amount = payment_history.payment_amount - total_utility_cost

        RefundHistory.objects.create(
            payment = payment_history,
            division = "H_Locker",
            date = payment_history.date,
            refund_date = today, #오늘
            fees = fees,
            oneday_cost = oneday_cost,
            used_period = used_period,
            used_amount = used_amount,
            total_utility_cost = total_utility_cost,
            refund_amount = refund_amount
        )
    elif payment_history.division == 'G_Locker':
        member.G_locker = None
        member.save()

        total_utility_cost = fees + used_amount
        refund_amount = payment_history.payment_amount - total_utility_cost

        RefundHistory.objects.create(
            payment = payment_history,
            division = "G_Locker",
            date = payment_history.date,
            refund_date = today, #오늘
            fees = fees,
            oneday_cost = oneday_cost,
            used_period = used_period,
            used_amount = used_amount,
            total_utility_cost = total_utility_cost,
            refund_amount = refund_amount
        )


    url = reverse('management:payment_history', kwargs={'member_id': member.id})
    return HttpResponseRedirect(url)


def staff_mypage(request, staff_id):
    staff = User.objects.get(id=staff_id)
    if staff.groups.filter(name__in=['FC']).exists():
        return redirect('mypage', staff_id=staff_id)

    elif staff.groups.filter(name__in=['Fitness']).exists():
        return redirect('PT_mypage', staff_id=staff_id)

    elif staff.groups.filter(name__in=['Pilates']).exists():
        return redirect('Pilates_mypage', staff_id=staff_id)
    else:
        return redirect('PT_mypage', staff_id=staff_id)


def edit_member(request, member_id):
    member = Member.objects.get(id=member_id)

    if request.method == 'POST':
        form = EditForm(request.POST or None, instance=member)
        if form.is_valid():
            form.save()
            return redirect('management:member_management')
    else:
        form = EditForm(instance=member)
    return render(request,'management/edit_member.html', {'form':form} )

def edit_staff(request, staff_id):
    staff = User.objects.get(id=staff_id)
    salary = Fitness_Salary.objects.filter(uid=staff_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=staff)

        if form.is_valid():
            form.save()
            return redirect('management:member_management')
    else:
        staff = User.objects.get(id=staff_id)
        form = CustomUserChangeForm(instance=staff)

    context = {
        'form' : form,
        'salary' : salary,
    }
    return render(request, 'management/edit_staff.html', context)

def staff_sales(request, staff_id):
    staff = User.objects.get(id=staff_id)
    if staff.groups.filter(name__in=['FC']).exists():
        salary = FC_Salary.objects.filter(uid=staff_id)

    elif staff.groups.filter(name__in=['Fitness']).exists():
        salary = Fitness_Salary.objects.filter(uid=staff_id)

    elif staff.groups.filter(name__in=['Pilates']).exists():
        salary = Pilates_Salary.objects.filter(uid=staff_id)
    else:
        pass

    context = {
        'staff' : staff,
        'salary' : salary,
    }
    return render(request, 'management/staff_sales.html', context)


def delete_member(request, member_id):
    member = Member.objects.get(id=member_id)
    member.delete()
    return redirect('management:member_management')


def delete_staff(request, staff_id):
    staff = User.objects.get(id=staff_id)
    staff.delete()
    return redirect('management:member_management')

def schedule_management(request):
    staff_list = User.objects.all()
    order_by = request.GET.get('order_by', 'groups')
    staff_list = User.objects.all().order_by(order_by)
    context = {
        'staff_list':staff_list,
    }
    return render(request, 'management/schedule_management.html', context)

def Fitness_schedule_management(request):
    Fitness_list = User.objects.filter(groups__name='Fitness') # Fitness 팀 직원들
    context = {
        'staff_list':Fitness_list,
    }
    return render(request, 'management/schedule_management.html', context)


def staff_schedule(request, staff_id):
    staff = User.objects.get(id=staff_id)
    schedules = staff.schedule.all() #나의 스케줄
    PT_members = staff.PT_members.all() #나의 PT 회원들
    Pil_members = staff.Pil_members.all() #나의 PT 회원들
    context = {
        'PT_members' : PT_members,
        'Pil_members': Pil_members,
        'schedules' : schedules,
        'staff' : staff,
    }
    return render(request, 'schedule.html', context)

def commission_management(request):
    FC_Teamleader_Com = FC_Teamleader_Commission.objects.all()
    FC_Personal_Com = FC_Personal_Commission.objects.all()
    FC_Personal_Com_1 = FC_Personal_Com.filter(personnel=1)
    FC_Personal_Com_2 = FC_Personal_Com.filter(personnel=2)
    FC_Personal_Com_3 = FC_Personal_Com.filter(personnel=3)
    FC_Team_Com = FC_Team_Commission.objects.all()
    Fit_Teamledaer_Com = Fitness_Teamledaer_Commission.objects.all()
    Fit_Personal_Com = Fitness_Personal_Commission.objects.all()
    Pil_Teamleader_Com = Pilates_Teamleader_Commission.objects.all()
    Pil_Com = Pilates_Commission.objects.all()
    Pil_GX_Basic = Pilates_GX_Basic.objects.all()
    Pil_GX_DependingNum = Pilates_GX_DependingNum.objects.all()
    Pil_PT = Pilates_PT.objects.all()
    context = {
        'FC_Teamleader_Com' : FC_Teamleader_Com,
        'FC_Personal_Com' : FC_Personal_Com,
        'FC_Personal_Com_1' : FC_Personal_Com_1,
        'FC_Personal_Com_2' : FC_Personal_Com_2,
        'FC_Personal_Com_3' : FC_Personal_Com_3,
        'FC_Team_Com' : FC_Team_Com,
        'Fit_Teamledaer_Com' : Fit_Teamledaer_Com,
        'Fit_Personal_Com' : Fit_Personal_Com,
        'Pil_Teamleader_Com' : Pil_Teamleader_Com,
        'Pil_Com' : Pil_Com,
        'Pil_GX_Basic' : Pil_GX_Basic,
        'Pil_GX_DependingNum' : Pil_GX_DependingNum,
        'Pil_PT' : Pil_PT,
    }

    return render(request, 'management/commission_management.html', context)

############커미션 수정

def fc_teamleader_edit_com(request, fc_teamleader_id):
    commission = FC_Teamleader_Commission.objects.get(id=fc_teamleader_id)

    if request.method == 'POST':
        form = FC_TeamLeader_EditForm(request.POST, instance=commission)

        if form.is_valid():
            form.save()
            return redirect('management:commission_management')
    else:
        commission = FC_Teamleader_Commission.objects.get(id=fc_teamleader_id)
        form = FC_TeamLeader_EditForm(instance=commission)

    context = {
        'form' : form,
    }
    return render(request, 'management/edit_commission.html', context)

def fc_team_edit_com(request, fc_team_id):
    commission = FC_Team_Commission.objects.get(id=fc_team_id)

    if request.method == 'POST':
        form = FC_Team_EditForm(request.POST, instance=commission)

        if form.is_valid():
            form.save()
            return redirect('management:commission_management')
    else:
        commission = FC_Team_Commission.objects.get(id=fc_teamleader_id)
        form = FC_Team_EditForm(instance=commission)

    context = {
        'form' : form,
    }
    return render(request, 'management/edit_commission.html', context)

def fc_personal_edit_com(request, fc_team_id):
    commission = FC_Personal_Commission.objects.get(id=fc_team_id)

    if request.method == 'POST':
        form = FC_Personal_EditForm(request.POST, instance=commission)

        if form.is_valid():
            form.save()
            return redirect('management:commission_management')
    else:
        commission = FC_Personal_Commission.objects.get(id=fc_team_id)
        form = FC_Personal_EditForm(instance=commission)

    context = {
        'form' : form,
    }
    return render(request, 'management/edit_commission.html', context)

def fit_teamleader_edit_com(request, fit_teamleader_id):
    commission = Fitness_Teamledaer_Commission.objects.get(id=fit_teamleader_id)

    if request.method == 'POST':
        form = Fit_TeamLeader_EditForm(request.POST, instance=commission)

        if form.is_valid():
            form.save()
            return redirect('management:commission_management')
    else:
        commission = Fitness_Teamledaer_Commission.objects.get(id=fit_teamleader_id)
        form = Fit_TeamLeader_EditForm(instance=commission)

    context = {
        'form' : form,
    }
    return render(request, 'management/edit_commission.html', context)

def fit_team_edit_com(request, fit_team_id):
    commission = Fitness_Personal_Commission.objects.get(id=fit_team_id)

    if request.method == 'POST':
        form = Fit_Personal_EditForm(request.POST, instance=commission)

        if form.is_valid():
            form.save()
            return redirect('management:commission_management')
    else:
        commission = Fitness_Personal_Commission.objects.get(id=fit_team_id)
        form = Fit_Personal_EditForm(instance=commission)

    context = {
        'form' : form,
    }
    return render(request, 'management/edit_commission.html', context)

def pil_teamleader_edit_com(request, pil_teamleader_id):
    commission = Pilates_Teamleader_Commission.objects.get(id=pil_teamleader_id)

    if request.method == 'POST':
        form = Pil_TeamLeader_EditForm(request.POST, instance=commission)

        if form.is_valid():
            form.save()
            return redirect('management:commission_management')
    else:
        commission = Pilates_Teamleader_Commission.objects.get(id=pil_teamleader_id)
        form = Pil_TeamLeader_EditForm(instance=commission)

    context = {
        'form' : form,
    }
    return render(request, 'management/edit_commission.html', context)

def pil_team_edit_com(request, pil_team_id):
    commission = Pilates_Commission.objects.get(id=pil_team_id)

    if request.method == 'POST':
        form = Pil_Team_EditForm(request.POST, instance=commission)

        if form.is_valid():
            form.save()
            return redirect('management:commission_management')
    else:
        commission = Pilates_Commission.objects.get(id=pil_team_id)
        form = Pil_Team_EditForm(instance=commission)

    context = {
        'form' : form,
    }
    return render(request, 'management/edit_commission.html', context)

def pil_pt_edit_com(request, fix_id):
    commission = Pilates_PT.objects.get(id=fix_id)

    if request.method == 'POST':
        form = Pil_PT_EditForm(request.POST, instance=commission)

        if form.is_valid():
            form.save()
            return redirect('management:commission_management')
    else:
        commission = Pilates_PT.objects.get(id=fix_id)
        form = Pil_PT_EditForm(instance=commission)

    context = {
        'form' : form,
    }
    return render(request, 'management/edit_commission.html', context)

def pil_dependingnum_edit_com(request, d_id):
    commission = Pilates_GX_DependingNum.objects.get(id=d_id)

    if request.method == 'POST':
        form = Pil_DependingNum_EditForm(request.POST, instance=commission)

        if form.is_valid():
            form.save()
            return redirect('management:commission_management')
    else:
        commission = Pilates_GX_DependingNum.objects.get(id=d_id)
        form = Pil_DependingNum_EditForm(instance=commission)

    context = {
        'form' : form,
    }
    return render(request, 'management/edit_commission.html', context)

def pil_gx_basic_edit_com(request, b_id):
    commission = Pilates_GX_Basic.objects.get(id=b_id)

    if request.method == 'POST':
        form = Pil_GX_basic_EditForm(request.POST, instance=commission)

        if form.is_valid():
            form.save()
            return redirect('management:commission_management')
    else:
        commission = Pilates_GX_Basic.objects.get(id=b_id)
        form = Pil_GX_basic_EditForm(instance=commission)

    context = {
        'form' : form,
    }
    return render(request, 'management/edit_commission.html', context)

##커미션 수정 끝

def sales_management(request):
    staff_list = User.objects.all()
    fc_list = User.objects.filter(groups__name='FC')
    context = {
        'staff_list':staff_list,
        'fc_list':fc_list,
    }
    return render(request, 'management/sales_management.html', context)

def set_today(request):
    if request.is_ajax():
        today = datetime.date.today().strftime('%Y-%m-%d')

        context = {
            'startdate' : today,
            'enddate' : today,
            'search_date' : today,
        }
    else:
        context = {
            'startdate' : today,
            'enddate' : today,
            'search_date':today,
        }
    return HttpResponse(json.dumps(context), content_type='application/json')

def sales_search(request):

    team_choice = request.GET.get('team_choice','') #선택된 팀 얻기. name으로 얻는듯
    startdate = request.GET.get('startdate','') #시작일 얻기
    enddate = request.GET.get('enddate','') #종료일 얻기
    lists=[]
    total=int(0)
    fc_total = int(0)
    fit_total= int(0)
    pil_total = int(0)
    all_total=int(0)

    if team_choice =='FC':
        team_members = User.objects.filter(groups__name='FC') # FC 팀 직원들
        for f in team_members:
            FC_members = f.payment_history.all() #결제내역 받아오기.
            members = FC_members.filter(date__range=[startdate, enddate])
            members_pay = members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00) if members else 0 # 회원들의 결제금액 합

            total = total + members_pay
            data = {'f':f, 'members_pay':members_pay}
            lists.append(data)

        context = {
            'lists':lists,
            'total':total,
            'startdate' : startdate if startdate else datetime.date.today(),
            'enddate' : enddate if startdate else datetime.date.today(),
            'team':team_choice,
        }

    elif team_choice =='Fitness' or team_choice =='Pilates':
        team_members = User.objects.filter(groups__name=team_choice) #피트니스 팀 직원들 or 필라테스 팀 직원들

        for f in team_members:
            PT_members = f.PT_members.all()
            members = PT_members.filter(PT_registered_date__range=[startdate, enddate])
            members_pay = members.aggregate(Sum('PT_payment_amount')).get('PT_payment_amount__sum',0.00) if members else 0 #Suspect some of members is None
            total = total + members_pay
            data = {'f':f, 'members_pay':members_pay}
            lists.append(data)

        context = {
            'lists':lists,
            'total':total,
            'startdate' : startdate if startdate else datetime.date.today(),
            'enddate' : enddate if startdate else datetime.date.today(),
            'team':team_choice,
        }

    else: #team_choice = 'All'
        fc_lists = []
        fit_lists = []
        pil_lists = []
        fc_list = User.objects.filter(groups__name='FC') # FC 팀 직원들
        Fitness_list = User.objects.filter(groups__name='Fitness') # Fitness 팀 직원들
        Pilates_list = User.objects.filter(groups__name='Pilates') # Pilates 팀 직원들

        for fc in fc_list:
            FC_members = fc.payment_history.all() #결제내역 받아오기.
            members = FC_members.filter(date__range=[startdate, enddate])
            fc_members_pay = members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00) if members else 0
            fc_total = fc_total + fc_members_pay
            data1 = {'fc':fc, "fc_members_pay" : fc_members_pay}
            fc_lists.append(data1)

        for fit in Fitness_list:
            PT_members = fit.PT_members.all()
            members = PT_members.filter(PT_registered_date__range=[startdate, enddate])
            fit_members_pay = members.aggregate(Sum('PT_payment_amount')).get('PT_payment_amount__sum',0.00) if members else 0
            fit_total = fit_total + fit_members_pay
            data2 = {'fit':fit, "fit_members_pay" : fit_members_pay}
            fit_lists.append(data2)

        for pil in Pilates_list:
            PT_members = pil.PT_members.all()
            members = PT_members.filter(PT_registered_date__range=[startdate, enddate])
            pil_members_pay = members.aggregate(Sum('PT_payment_amount')).get('PT_payment_amount__sum',0.00) if members else 0
            pil_total = pil_total+pil_members_pay
            data3 = {'pil':pil, "pil_members_pay" : pil_members_pay}
            pil_lists.append(data3)

        all_total = fc_total + fit_total + pil_total
        context = { #'All'의 context
            'fc':  fc_list.count()+1, #템플릿에서 한칸더 rowspan해야하기 때문에 +1
            'fit':  Fitness_list.count()+1,
            'pil':  Pilates_list.count()+1,

            'fc_lists':fc_lists,
            'fit_lists':fit_lists,
            'pil_lists':pil_lists,

            'fc_total': fc_total,
            'fit_total' : fit_total,
            'pil_total' : pil_total,
            'total': all_total,

            'startdate' : startdate if startdate else datetime.date.today(),
            'enddate' : enddate if startdate else datetime.date.today(),
            'team':team_choice,
        }
    return render(request, 'management/sales_management.html', context)


def fitness_daily_schedule(request):
    today = datetime.date.today()
    Fitness_list = User.objects.filter(groups__name='Fitness') # Fitness 팀 직원들
    schedules= Schedule.objects.none()
    trainer_dict = OrderedDict()

    for f in Fitness_list:
        trainer_dict[str(f)] = {'name' : f, 'hour_21':'', 'hour_22':'', 'hour_23':'', 'hour_0':'', 'hour_1':'','hour_2':'','hour_3':'','hour_4':'','hour_5':'','hour_6':'','hour_7':'','hour_8':'','hour_9':'','hour_10':'','hour_11':'','hour_12':'','hour_13':'','hour_14':'',}

        sc = f.schedule.filter(start__year=today.year).filter(start__month = today.month).filter(start__day = today.day) #오늘
        schedules |= sc

    for sc in schedules:
        trainer_dict[str(sc.Trainer)]['hour_'+str(sc.start.hour)] = sc.title

    trainer_dict = trainer_dict.items()


    context = {
        'Fitness_list':Fitness_list,
        'trainer_dict' : trainer_dict,
        'search_date' : datetime.date.today()
    }
    return render(request, 'management/fitness_daily_schedule.html', context)

def fitness_daily_schedule_search(request):

    all_schedules = Schedule.objects.all()
    Fitness_list = User.objects.filter(groups__name='Fitness') # Fitness 팀 직원들

    search_date1 = request.GET.get('search_date','') #날짜 얻기
    search_date= datetime.datetime.strptime(search_date1, '%Y-%m-%d')

    schedules= Schedule.objects.none()
    trainer_dict = OrderedDict()

    for f in Fitness_list:
        trainer_dict[str(f)] = {'name' : f, 'hour_21':'', 'hour_22':'', 'hour_23':'', 'hour_0':'', 'hour_1':'','hour_2':'','hour_3':'','hour_4':'','hour_5':'','hour_6':'','hour_7':'','hour_8':'','hour_9':'','hour_10':'','hour_11':'','hour_12':'','hour_13':'','hour_14':'',}

        sc = f.schedule.filter(start__year=search_date.year).filter(start__month = search_date.month).filter(start__day = search_date.day)
        schedules |= sc


    for sc in schedules:
        trainer_dict[str(sc.Trainer)]['hour_'+str(sc.start.hour)] = sc.title

    trainer_dict = trainer_dict.items()

    context = {
        'all_schedules' : all_schedules,
        'search_date' : search_date1 if search_date1 else datetime.date.today(),
        'Fitness_list':Fitness_list,
        'trainer_dict' : trainer_dict
    }
    return render(request, 'management/fitness_daily_schedule.html', context)

def pilates_daily_schedule(request):
    today = datetime.date.today()
    Pilates_list = User.objects.filter(groups__name='Pilates') # Pilates 팀 직원들
    schedules= Schedule.objects.none()
    trainer_dict = OrderedDict()

    for f in Pilates_list:
        trainer_dict[str(f)] = {'name' : f, 'hour_21':'', 'hour_22':'', 'hour_23':'', 'hour_0':'', 'hour_1':'','hour_2':'','hour_3':'','hour_4':'','hour_5':'','hour_6':'','hour_7':'','hour_8':'','hour_9':'','hour_10':'','hour_11':'','hour_12':'','hour_13':'','hour_14':'',}

        sc = f.schedule.filter(start__year=today.year).filter(start__month = today.month).filter(start__day = today.day) #오늘
        schedules |= sc

    for sc in schedules:
        trainer_dict[str(sc.Trainer)]['hour_'+str(sc.start.hour)] = sc.title

    trainer_dict = trainer_dict.items()


    context = {
        'Pilates_list':Pilates_list,
        'trainer_dict' : trainer_dict,
        'search_date' : datetime.date.today()
    }
    return render(request, 'management/pilates_daily_schedule.html', context)

def pilates_daily_schedule_search(request):

    all_schedules = Schedule.objects.all()
    Pilates_list = User.objects.filter(groups__name='Pilates') # Pilates 팀 직원들

    search_date1 = request.GET.get('search_date','') #날짜 얻기
    search_date= datetime.datetime.strptime(search_date1, '%Y-%m-%d')

    schedules= Schedule.objects.none()
    trainer_dict = OrderedDict()

    for f in Pilates_list:
        trainer_dict[str(f)] = {'name' : f, 'hour_21':'', 'hour_22':'', 'hour_23':'', 'hour_0':'', 'hour_1':'','hour_2':'','hour_3':'','hour_4':'','hour_5':'','hour_6':'','hour_7':'','hour_8':'','hour_9':'','hour_10':'','hour_11':'','hour_12':'','hour_13':'','hour_14':'',}

        sc = f.schedule.filter(start__year=search_date.year).filter(start__month = search_date.month).filter(start__day = search_date.day)
        schedules |= sc


    for sc in schedules:
        trainer_dict[str(sc.Trainer)]['hour_'+str(sc.start.hour)] = sc.title

    trainer_dict = trainer_dict.items()

    context = {
        'all_schedules' : all_schedules,
        'search_date' : search_date1 if search_date1 else datetime.date.today(),
        'Pilates_list':Pilates_list,
        'trainer_dict' : trainer_dict
    }
    return render(request, 'management/pilates_daily_schedule.html', context)