from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.db import models



class User(AbstractUser):
    sex = models.CharField(max_length=12, verbose_name='성별',null=True)
    birth = models.DateField(null=True, blank=True)
    phone_num = models.CharField(max_length=32, null=True, help_text='Ex) 010-1234-1234',verbose_name='휴대번호')
    teamleader = models.BooleanField(blank=True, default=False, verbose_name='팀장 여부')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=0, default=0 ,verbose_name='기본급')
    pilates_GX = models.CharField(max_length=32, blank=True, null=True, help_text='필라테스 gx정책',verbose_name='필라테스 GX정책')
    pilates_PT = models.CharField(max_length=32, blank=True, null=True, help_text='필라테스 PT정책',verbose_name='필라테스 PT정책')

class FC_Salary(models.Model):
    uid = models.IntegerField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='이름', related_name='FC_Salary')
    date = models.DateField(verbose_name='날짜')
    number = models.IntegerField(blank=True, null=True, verbose_name='팀 인원')
    team_sales = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='팀 매출')
    personal_sales = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='개인 매출')
    FC_refund = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='FC팀 총 환불')
    personal_refund = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='개인 환불')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='기본급')
    commission_rate = models.FloatField(default=0.0, blank=True, verbose_name='팀커미션 비율')
    commission =  models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='팀커미션')
    personal_commission_rate = models.FloatField(default=0.0,blank=True, verbose_name='개인 커미션 비율')
    personal_commission = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='개인 커미션')
    salary = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='월급')

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['date']


class Fitness_Salary(models.Model):
    uid = models.IntegerField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='이름', related_name='Fitness_Salary')
    date = models.DateField(verbose_name='날짜')
    team_sales = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='팀 매출')
    personal_sales = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='개인 매출')
    Fitness_refund = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='Fitness팀 총 환불')
    personal_refund = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='개인 환불')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='기본급')
    commission_rate = models.FloatField(default=0.0, verbose_name='커미션 비율')
    commission =  models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='커미션')
    tuition_rate =  models.IntegerField(default=0, verbose_name='수업료 비율')
    tuition = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='수업료')
    salary = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='월급')

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['date']

class Pilates_Salary(models.Model):
    uid = models.IntegerField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='이름', related_name='Pilates_Salary')
    date = models.DateField(verbose_name='날짜')
    team_sales = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='팀 매출')
    personal_sales = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='개인 매출')
    Pilates_refund = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='Pilates팀 총 환불')
    personal_refund = models.DecimalField(max_digits=19, decimal_places=0,blank=True, default=0,verbose_name='개인 환불')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='기본급')
    commission_rate = models.FloatField(default=0.0, blank=True, verbose_name='커미션 비율')
    commission =  models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='커미션')
    GX_commission = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='GX 커미션')
    PT_commission_rate = models.FloatField(default=0.0, blank=True, verbose_name='PT 커미션 비율')
    PT_commission = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='PT 커미션')
    total = models.DecimalField(max_digits=12, decimal_places=0,blank=True, default=0,verbose_name='합계')
    refund = models.DecimalField(max_digits=10, decimal_places=0,blank=True, null=True, default=0,verbose_name='환불 합계')
    salary = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='월급')

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['date']




