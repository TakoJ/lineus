from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from authentication.models import User
from staff.models import Member
from management.forms import CustomUserChangeForm, EditForm
import datetime
import json

# Create your views here.

def member_management(request):
    staff_list = User.objects.all()
    member_list = Member.objects.all()
    context = {
        'staff_list':staff_list,
        'member_list' : member_list,
    }
    return render(request, 'management/member_management.html', context)

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
    }
    return render(request, 'management/edit_staff.html', context)

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
    context = {
        'staff_list':staff_list,
    }
    return render(request, 'management/schedule_management.html', context)

def staff_schedule(request, staff_id):
    staff = User.objects.get(id=staff_id)
    schedules = staff.schedule.all() #나의 스케줄
    PT_members = staff.PT_members.all() #나의 PT 회원들
    context = {
        'PT_members' : PT_members,
        'schedules' : schedules,
    }
    return render(request, 'schedule.html', context)

def commission_management(request):
    return render(request, 'management/commission_management.html')

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
        startdate = datetime.date.today()
        enddate = datetime.date.today()

        context = {
            'startdate' : startdate.strftime('%Y-%m-%d'),
            'enddate' : enddate.strftime('%Y-%m-%d'),
        }
    else:
        context = {
            'startdate' : datetime.date.today().strftime('%Y-%m-%d'),
            'enddate' : datetime.date.today().strftime('%Y-%m-%d')
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
            FC_members = f.members.all()
            members = FC_members.filter(start_date__range=[startdate, enddate])
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
            members = PT_members.filter(registered_date__range=[startdate, enddate])
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
            FC_members = fc.members.all()
            members = FC_members.filter(start_date__range=[startdate, enddate])
            fc_members_pay = members.aggregate(Sum('payment_amount')).get('payment_amount__sum',0.00) if members else 0
            fc_total = fc_total + fc_members_pay
            data1 = {'fc':fc, "fc_members_pay" : fc_members_pay}
            fc_lists.append(data1)

        for fit in Fitness_list:
            PT_members = fit.PT_members.all()
            members = PT_members.filter(registered_date__range=[startdate, enddate])
            fit_members_pay = members.aggregate(Sum('PT_payment_amount')).get('PT_payment_amount__sum',0.00) if members else 0
            fit_total = fit_total + fit_members_pay
            data2 = {'fit':fit, "fit_members_pay" : fit_members_pay}
            fit_lists.append(data2)

        for pil in Pilates_list:
            PT_members = pil.PT_members.all()
            members = PT_members.filter(registered_date__range=[startdate, enddate])
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

