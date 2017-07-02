from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta, datetime

class Member(models.Model):
    name = models.CharField(max_length=24, verbose_name='성명')
    birth = models.DateField(null=True,help_text='Ex) 1980-06-30',verbose_name='생년월일')
    phone_regex = RegexValidator(regex=r'^\d{2,3}-\d{3,4}-\d{4}$', message="휴대폰 양식으로 써주세요.")
    phone_num = models.CharField(validators=[phone_regex], max_length=32, null=True, help_text='Ex) 010-1234-1234',verbose_name='휴대번호')
    address = models.CharField(max_length=64,blank=True, null=True,verbose_name='주소')
    sex = models.CharField(max_length=12,verbose_name='성별',null=True)
    start_date = models.DateField(default=timezone.now, verbose_name='등록일')
    end_date = models.DateField(default=(datetime.now() + timedelta(days=30)), verbose_name='회원권종료일')
    #Staff와 1:n 관계, staff삭제시 null값적용
    staff = models.ForeignKey(User, null=True, related_name='members', on_delete=models.SET_NULL)

    # 회원권 세부사항
    type_choice = models.CharField(max_length=12,default='피트니스',verbose_name='종류선택')
    rating = models.CharField(max_length=12, default='Bronze',verbose_name='등급')
    period_fitness = models.CharField(max_length=12,null=True, blank=True,verbose_name='피트니스기간', help_text='피트니스를 선택하신분만 선택해주세요.')
    period_pilates = models.CharField(max_length=12, null=True, blank=True,verbose_name='필라테스기간', help_text='필라테스를 선택하신분만 선택해주세요.')
    period_both = models.CharField(max_length=12, null=True, blank=True, verbose_name="피트니스+필라테스기간")
    locker=models.CharField(max_length=12,blank=True,null=True,verbose_name='추가사항', help_text='락카를 쓰실 분만 선택해주세요. 헬스락카는 H, 골프락카는 G')
    period_locker=models.IntegerField(null=True,blank=True, verbose_name='락카개월수', help_text='락카를 쓰실 분만 입력해주세요. 락카를 사용할 개월수를 적어주세요.')
    cautions = models.CharField(max_length=128,blank=True,verbose_name='병력및주의사항')
    exercise_time = models.CharField(max_length=12, blank=True,verbose_name='운동시간대')
    visit_path = models.CharField(max_length=12, blank=True,verbose_name='방문경로')
    payment_amount = models.DecimalField(max_digits=10,decimal_places=0, default=0 ,verbose_name='결제금액')
    payment_method = models.CharField(max_length=12,default='카드',verbose_name='결제방식')

    #PT
    SESSION_CHOICES = (
        ('10세션/60일','10세션/60일'),
        ('20세션/90일','20세션/90일'),
    )
    Trainer = models.ForeignKey(User, null=True, blank=True, related_name='PT_members', on_delete=models.SET_NULL)
    registered_session = models.CharField(max_length=24, blank=True,verbose_name='등록세션')
    PT_payment_amount = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='PT결제금액')
    PT_payment_method = models.CharField(max_length=12,blank=True ,verbose_name='PT결제방식')
    unitprice = models.DecimalField(max_digits=10, decimal_places=0,blank=True, null=True, verbose_name='1회세션단가')
    period_PT = models.CharField(max_length=12,blank=True, null=True,verbose_name='강습기간')


    def __str__(self):
        return self.name

    def save(self):
        from datetime import datetime, timedelta

        #중복 문장줄어야 하는데, 따로 빼면 선언이 안되있다는 오류남
        if self.period_fitness=="m1" or self.period_pilates=='se2m1' or self.period_pilates=='se3m1' or self.period_both=='se2m1' or self.period_both=='se3m1':
            d = 30
            days = timedelta(days=d)
            self.end_date = datetime.now() + days
            super(Member, self).save()

        elif self.period_fitness=='m3' or self.period_pilates=='se2m3' or self.period_pilates=='se3m3' or self.period_both=='se2m3' or self.period_both=='se3m3':
            d=90
            days = timedelta(days=d)
            self.end_date = datetime.now() + days
            super(Member, self).save()

        elif self.period_fitness=='m6' or self.period_pilates=='se2m6' or self.period_pilates=='se3m6' or self.period_both=='se2m6' or self.period_both=='se3m6':
            d=180
            days = timedelta(days=d)
            self.end_date = datetime.now() + days
            super(Member, self).save()

        elif self.period_fitness=='m12':
            d=365
            days = timedelta(days=d)
            self.end_date = datetime.now() + days
            super(Member, self).save()
        else:
            d=0


