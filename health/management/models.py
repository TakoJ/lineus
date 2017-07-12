from django.db import models

# Create your models here.

class FC_Teamleader_Commission(models.Model): #FC팀장님의 수장(팀수당만 있음.)
    min_sales = models.DecimalField(max_digits=19,decimal_places=0, default=0 ,verbose_name='FC 팀매출 범위 시작')
    max_sales = models.DecimalField(max_digits=19,decimal_places=0, blank=True, null=True, verbose_name='FC팀매출 범위 종료')
    commission = models.FloatField(default=0.0, verbose_name='커미션')

    def __str__(self):
        return str(self.min_sales)

    #퍼센트로 만들기
    @property
    def percent(self):
        return float(self.commission /100)

class FC_Personal_Commission(models.Model): #FC팀의 개인수당
    min_personal_sales = models.DecimalField(max_digits=19,decimal_places=0, default=0 ,verbose_name='FC 개인매출범위 시작')
    max_personal_sales = models.DecimalField(max_digits=19,decimal_places=0, blank=True, null=True, verbose_name='FC 개인 매출범위 종료')
    personnel = models.IntegerField(null=True, verbose_name='인원')
    commission = models.FloatField(default=0.0, verbose_name='커미션')

    def __str__(self):
        return str(self.min_personal_sales)

    #퍼센트로 만들기
    @property
    def percent(self):
        return float(self.commission /100)

class FC_Team_Commission(models.Model): #FC팀의 팀수당
    min_sales = models.DecimalField(max_digits=19,decimal_places=0, default=0 ,verbose_name='FC 팀매출 범위 시작')
    max_sales = models.DecimalField(max_digits=19,decimal_places=0, blank=True, null=True, verbose_name='FC 팀매출 범위 종료')
    commission = models.FloatField(default=0.0, verbose_name='커미션')

    def __str__(self):
        return str(self.min_sales)

    #퍼센트로 만들기
    @property
    def percent(self):
        return float(self.commission /100)

class Fitness_Teamledaer_Commission(models.Model): #피트니스 팀장님의 팀 수당, 수업료는 50%
    min_sales = models.DecimalField(max_digits=19,decimal_places=0, default=0 ,verbose_name='Fitness 팀매출 범위 시작')
    max_sales = models.DecimalField(max_digits=19,decimal_places=0, blank=True, null=True, verbose_name='Fitness 팀매출 범위 종료')
    commission = models.FloatField(default=0.0, verbose_name='커미션')
    tuition_commission = models.IntegerField(default=50, verbose_name='수업료 비율') #현재 매출에 상관없이 50%

    def __str__(self):
        return str(self.min_sales)
    #퍼센트로 만들기
    @property
    def percent(self):
        return float(self.commission /100)

class Fitness_Personal_Commission(models.Model): #피트니스 팀의 수당(개인수당만 존재)
    min_personal_sales = models.DecimalField(max_digits=19,decimal_places=0, default=0 ,verbose_name='Fitness 개인매출 범위 시작')
    max_personal_sales = models.DecimalField(max_digits=19,decimal_places=0, blank=True, null=True, verbose_name='Fitness 팀매출 범위 종료')
    commission = models.FloatField(default=0.0, verbose_name='커미션')
    tuition_commission = models.IntegerField(default=0, verbose_name='수업료 비율')

    def __str__(self):
        return str(self.min_personal_sales)

    #퍼센트로 만들기
    @property
    def percent(self):
        return float(self.commission /100)

class Pilates_Teamleader_Commission(models.Model): #필라테스 팀장님의 수당(팀 수당만 존재)
    min_sales = models.DecimalField(max_digits=19,decimal_places=0, default=0 ,verbose_name='Pilates 팀매출 범위 시작')
    max_sales = models.DecimalField(max_digits=19,decimal_places=0, blank=True, null=True, verbose_name='Fitness 팀매출 범위 종료')
    commission = models.FloatField(default=0.0, verbose_name='커미션')
    tuition = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=30000,verbose_name='수업당 수업비')
    #현재 필라테스 팀장님 수업비 수업당 3만원.
    #
    #문제는 지금 GX는 몇번했는지 안만들어놨음 PT는 스케줄갯수지만.GX는?? PILATES GX 모델(trainer, 명수)만들어야할듯

    def __str__(self):
        return str(self.min_sales)

    #퍼센트로 만들기
    @property
    def percent(self):
        return float(self.commission /100)

class Pilates_Commission(models.Model): #필라테스 팀의 수당(개인 수당만 존재)
    min_personal_sales = models.DecimalField(max_digits=19,decimal_places=0, default=0 ,verbose_name='Pilates 개인매출 범위 시작')
    max_personal_sales = models.DecimalField(max_digits=19,decimal_places=0, default=0 ,verbose_name='Pilates 개인매출 범위 종료')
    tuition_commission = models.FloatField(default=30.0, verbose_name='수업료 비율') #파트타임 트레이너는 항상 40%

    tuition = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=20000,verbose_name='수업당 수업비')
    #파트, 오전 트레이너는 2만원/ 오후는 GX명수에 따라 달라짐.

    def __str__(self):
        return str(self.min_personal_sales)

    #퍼센트로 만들기
    @property
    def percent(self):
        return float(self.commission /100)