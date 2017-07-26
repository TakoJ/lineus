from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta, datetime

class Member(models.Model):
    SEX_CHOICES = (
        ('M','남자'),
        ('F','여자'),
    )
    STATUS_CHOICES = (
        ('new','신규'),
        ('re','재등록'),
        )
    #charfield에 choices= 넣으면 회원가입이 안된다. 왜지?
    division = models.CharField(max_length=12, default="new", verbose_name='회원구분')
    name = models.CharField(max_length=24, verbose_name='성명')
    birth = models.DateField(null=True,help_text='Ex) 1980-06-30',verbose_name='생년월일')
    phone_regex = RegexValidator(regex=r'^\d{2,3}-\d{3,4}-\d{4}$', message="휴대폰 양식으로 써주세요.")
    phone_num = models.CharField(validators=[phone_regex], max_length=32, null=True, help_text='Ex) 010-1234-1234',verbose_name='휴대번호')
    address = models.CharField(max_length=64,blank=True, null=True,verbose_name='주소')
    sex = models.CharField(max_length=12, verbose_name='성별',null=True)
    registered_date = models.DateField(blank=True, default=timezone.now, verbose_name='등록일')
    start_date = models.DateField(default=timezone.now, blank=True, verbose_name='시작일')
    end_date = models.DateField(blank=True, verbose_name='회원권종료일')
    #Staff와 1:n 관계, staff삭제시 null값적용
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='members', on_delete=models.SET_NULL)

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
    membership_amount = models.DecimalField(max_digits=10,decimal_places=0, default=0 ,verbose_name='회원권 금액')
    locker_amount = models.DecimalField(max_digits=10,decimal_places=0, default=0 ,verbose_name='락카 금액')
    payment_amount = models.DecimalField(max_digits=10,decimal_places=0, default=0 ,verbose_name='결제금액')
    payment_method = models.CharField(max_length=12,default='카드',verbose_name='결제방식')
    note = models.TextField(blank=True, null=True, verbose_name='비고란')

    #PT(Fitness)
    Trainer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='PT_members', on_delete=models.SET_NULL)
    registered_session = models.IntegerField(null=True, blank=True,verbose_name='등록세션')
    PT_payment_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0,verbose_name='PT결제금액')
    PT_payment_method = models.CharField(max_length=12, null=True, blank=True ,verbose_name='PT결제방식')
    unitprice = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='1회세션단가')
    period_PT = models.CharField(max_length=12,blank=True, null=True,verbose_name='강습기간')
    PT_registered_date = models.DateField(null=True, blank=True, verbose_name='PT등록일')

    OT_used_session = models.IntegerField(blank=True, null=True, default=0, verbose_name='OT 횟수')
    used_session = models.IntegerField(blank=True, null=True, default=0, verbose_name='사용한 세션')
    re_registered = models.BooleanField(blank=True, default=False, verbose_name='PT재등록 여부')

    #Pt(Pilates)
    Pil_Trainer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='Pil_members', on_delete=models.SET_NULL)
    Pil_registered_session = models.IntegerField(null=True, blank=True,verbose_name='Pilates 등록세션')
    Pil_payment_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0,verbose_name='Pilates 결제금액')
    Pil_payment_method = models.CharField(max_length=12, null=True, blank=True ,verbose_name='Pilates 결제방식')
    Pil_unitprice = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='Pilates 1회세션단가')
    Pil_period_PT = models.CharField(max_length=12,blank=True, null=True,verbose_name='Pilates 강습기간')
    Pil_registered_date = models.DateField(null=True, blank=True, verbose_name='Pilates 등록일')

    Pil_OT_used_session = models.IntegerField(blank=True, null=True, default=0, verbose_name='Pilates OT 횟수')
    Pil_used_session = models.IntegerField(blank=True, null=True, default=0, verbose_name='Pilates 사용한 세션')
    Pil_re_registered = models.BooleanField(blank=True, default=False, verbose_name='Pilates재등록 여부')

    #회원권,pt권 활성,만료, 환불 여부
    Membership_status = models.IntegerField(blank=True, null=True, default=1)#1이면 활성, 0면 비활성(만료). 환불시 2
    PT_status = models.IntegerField(blank=True, null=True, default=0)#1이면 활성, 0면 비활성(만료). 환불시 2
    Pil_status = models.IntegerField(blank=True, null=True, default=0)#1이면 활성, 0면 비활성(만료). 환불시 2



    def __str__(self):
        return self.name

    # 수수로(10%)를 제외한 1회세션단가
    @property
    def PT_unitprice(self):
        return int(self.unitprice * 10/11) #소수점없이 반환

class MembershipHistory(models.Model):
    user = models.ForeignKey(Member, null=True, verbose_name='회원', related_name='MembershipHistory') #Member

    division = models.CharField(max_length=12, default="신규", verbose_name='회원구분')
    birth = models.DateField(null=True,help_text='Ex) 1980-06-30',verbose_name='생년월일')
    phone_regex = RegexValidator(regex=r'^\d{2,3}-\d{3,4}-\d{4}$', message="휴대폰 양식으로 써주세요.")
    phone_num = models.CharField(validators=[phone_regex], max_length=32, null=True, help_text='Ex) 010-1234-1234',verbose_name='휴대번호')
    address = models.CharField(max_length=64,blank=True, null=True,verbose_name='주소')
    sex = models.CharField(max_length=12, verbose_name='성별',null=True)
    registered_date = models.DateField(blank=True, default=timezone.now, verbose_name='등록일')
    start_date = models.DateField(default=timezone.now, blank=True, verbose_name='시작일')
    end_date = models.DateField(blank=True, verbose_name='회원권종료일')
    #Staff와 1:n 관계, staff삭제시 null값적용
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='history_members', on_delete=models.SET_NULL)

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
    membership_amount = models.DecimalField(max_digits=10,decimal_places=0, default=0 ,verbose_name='회원권 금액')
    locker_amount = models.DecimalField(max_digits=10,decimal_places=0, default=0 ,verbose_name='락카 금액')
    payment_amount = models.DecimalField(max_digits=10,decimal_places=0, default=0 ,verbose_name='결제금액')
    payment_method = models.CharField(max_length=12,default='카드',verbose_name='결제방식')
    note = models.TextField(blank=True, null=True, verbose_name='비고란')



class PaymentHistory(models.Model):
    user = models.ForeignKey(Member, null=True, verbose_name='회원', related_name='PaymentHistory') #Member
    uid = models.IntegerField(null=True) #user의 id도 가져오자.
    division = models.CharField(max_length=12, null=True, verbose_name="회원권/Fitness/Pilates 구분") #회원권 = 'Membership'
    date = models.DateField(verbose_name='결제일')
    start_date = models.DateField(blank=True, verbose_name='시작일') #회원권 등록 환불때필요.
    end_date = models.DateField(blank=True, verbose_name='회원권종료일')
    registered_session = models.IntegerField(null=True, blank=True,verbose_name='등록세션')
    payment_amount = models.DecimalField(max_digits=10,decimal_places=0, default=0 ,verbose_name='결제금액')
    status = models.IntegerField(default=1) #1이면 활성, 0면 비활성. end_date와 today비교해서 비활성. 환불시 2

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        self.uid = self.user.id #user의 uid 자동 저장
        super(PaymentHistory, self).save(*args, **kwargs)

class RefundHistory(models.Model):
    payment = models.OneToOneField(PaymentHistory, related_name="refund")
    division = models.CharField(max_length=12, null=True,blank=True, verbose_name="회원권/Fitness/Pilates 구분") #회원권 = 'Membership', Fitness="Fitness", Pilates="Pilates"
    date = models.DateField(null=True, verbose_name='결제일')
    refund_date = models.DateField(verbose_name='환불일')
    fees = models.DecimalField(max_digits=10,blank=True, null=True, decimal_places=0 ,verbose_name='수수료')
    refund = models.DecimalField(max_digits=10,decimal_places=0, blank=True, null=True, default=0 ,verbose_name='환불금액')
    refund_amount = models.DecimalField(max_digits=10,decimal_places=0, default=0 ,verbose_name='총합')

class History(models.Model): #pt history
    user = models.ForeignKey(Member, max_length=12, verbose_name='성명', related_name='History') #ForeignKey로 하면 def __str__에서 오류 난다.
    birth = models.DateField(null=True, blank=True,help_text='Ex) 1980-06-30',verbose_name='생년월일') #동명이인을 구별하기 위해 추가
    division = models.CharField(max_length=12, null=True,blank=True, verbose_name="PT 구분") #
    Trainer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='Trainer', on_delete=models.SET_NULL)
    registered_session = models.CharField(max_length=24, blank=True,verbose_name='등록세션')
    PT_payment_amount = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='PT결제금액')
    PT_payment_method = models.CharField(max_length=12,blank=True ,verbose_name='PT결제방식')
    unitprice = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='1회세션단가')
    period_PT = models.CharField(max_length=12,blank=True, null=True,verbose_name='강습기간')
    PT_registered_date = models.DateField(blank=True, verbose_name='PT등록일')
    Num = models.IntegerField(default=0)

class Pil_History(models.Model): #pilates history
    user = models.ForeignKey(Member, max_length=12, verbose_name='성명', related_name='Pil_History') #ForeignKey로 하면 def __str__에서 오류 난다.
    birth = models.DateField(null=True, blank=True,help_text='Ex) 1980-06-30',verbose_name='생년월일') #동명이인을 구별하기 위해 추가
    division = models.CharField(max_length=12, null=True,blank=True, verbose_name="PT 구분")
    Pil_Trainer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='Pil_Trainer', on_delete=models.SET_NULL)
    Pil_registered_session = models.CharField(max_length=24, blank=True,verbose_name='Pilates 등록세션')
    Pil_payment_amount = models.DecimalField(max_digits=10, decimal_places=0,blank=True, default=0,verbose_name='Pilates 결제금액')
    Pil_payment_method = models.CharField(max_length=12,blank=True ,verbose_name='Pilates 결제방식')
    Pil_unitprice = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='Pil_1회세션단가')
    Pil_period_PT = models.CharField(max_length=12,blank=True, null=True,verbose_name='Pil_강습기간')
    Pil_registered_date = models.DateField(blank=True, verbose_name='Pilates 등록일')
    Num = models.IntegerField(default=0)



class Schedule(models.Model):
    Trainer = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True, related_name='schedule', on_delete=models.SET_NULL)
    title = models.CharField(max_length=12,blank=True,)
    name = models.ForeignKey(Member, null=True, verbose_name='회원이름')
    birth = models.DateField(null=True,blank=True,help_text='Ex) 1980-06-30',verbose_name='생년월일') #동명이인을 구별하기 위해 추가
    PT_registered_date = models.DateField(null=True, blank=True, verbose_name='해당PT등록일')
    # 다른 pt등록과 구분하기 위해(즉 어떤 history인지)
    registered_session = models.CharField(max_length=24, null=True, blank=True,verbose_name='등록세션')
    OT_used_session = models.IntegerField(blank=True, null=True, default=0, verbose_name='OT 횟수')
    used_session = models.IntegerField(blank=True, null=True, default=0, verbose_name='사용한 세션')
    unitprice = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, default=0, verbose_name='1회세션단가')

    #pilates GX
    GX = models.BooleanField(blank=True, default=False, verbose_name='GX 여부')
    number = models.IntegerField(blank=True, null=True, verbose_name='GX명수')

    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(blank=True,null=True) #optional


    def get_year(self):
        return self.start.year
    def get_month(self):
        return self.start.month-1 ##how apout "0"+
    def get_day(self):
        return self.start.day
    def get_hour(self):
        # return DateTimeFormat(start, "%H")
        return self.start.hour #왜 9시간뒤로가지?
    def get_minute(self):
        return self.start.minute

    def __str__(self):
        return self.title


