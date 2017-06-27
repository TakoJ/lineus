from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.timezone import now


class Staff(models.Model):
    name = models.CharField(max_length=24)
    job = models.CharField(max_length=24)

    def __str__(self):
        return str(self.name)

class Member(models.Model):
    SEX_CHOICES = (
        ('M','남자'),
        ('F','여자'),
    )
    LOCKER_CHOICES = (
        ('H','H'),
        ('G','G'),
    )
    TYPE_CHOICES = (
        ('Fitness','피트니스'),
        ('Pilates','필라테스'),
        ('Both','피트니스+필라테스'),
    )
    RATING_CHOICES = (
        ('B','Bronze'),
        ('S','Silver'),
        ('G','Gold'),
        ('VIP','VIP'),
    )
    FITNESS_CHOICES = (
        ('1개월','1개월'),
        ('3개월','3개월'),
        ('6개월','6개월'),
        ('12개월','12개월'),
    )
    PILATES_CHOICES = (
        ('주 2회 4주','주 2회 4주'),
        ('주 3회 4주','주 3회 4주'),
        ('주 2회 12주','주 2회 12주'),
        ('주 3회 12주','주 3회 12주'),
        ('주 2회 24주','주 2회 24주'),
        ('주 3회 24주','주 3회 24주'),
    )
    PAYMENT_CHOICES = (
        ('현금','현금'),
        ('카드','카드'),
    )
    #인적사항
    성명 = models.CharField(max_length=24)
    생년월일 = models.DateField(null=True,help_text='Ex) 1980-06-30')
    phone_regex = RegexValidator(regex=r'^\d{2,3}-\d{3,4}-\d{4}$', message="휴대폰 양식으로 써주세요.")
    휴대번호 = models.CharField(validators=[phone_regex], max_length=32, null=True, help_text='Ex) 010-1234-1234')
    주소 = models.CharField(max_length=64,blank=True, null=True)
    성별 = models.CharField(max_length=12)
    등록일 = models.DateField(default=timezone.now)
    #Staff와 1:n 관계, staff삭제시 null값적용
    staff = models.ForeignKey(User, null=True, related_name='members', on_delete=models.SET_NULL)

    # 회원권 세부사항
    종류선택 = models.CharField(max_length=12,default='피트니스')
    등급 = models.CharField(max_length=12, default='Bronze')
    피트니스기간 = models.CharField(max_length=12, null=True, blank=True, help_text='피트니스를 선택하신분만 선택해주세요.')
    필라테스기간 = models.CharField(max_length=12, null=True, blank=True, help_text='필라테스를 선택하신분만 선택해주세요.')
    추가사항=models.CharField(max_length=12,blank=True,null=True, help_text='락카를 쓰실 분만 선택해주세요. 헬스락카는 H, 골프락카는 G')
    락카개월수=models.IntegerField(null=True,blank=True,help_text='락카를 쓰실 분만 입력해주세요. 락카를 사용할 개월수를 적어주세요.')
    병력및주의사항 = models.CharField(max_length=128,blank=True)
    운동시간대 = models.CharField(max_length=12, blank=True)
    결제금액 = models.DecimalField(max_digits=10,decimal_places=0, default=0)
    결제방식 = models.CharField(max_length=12,default='카드')


    def __str__(self):
        return self.성명


