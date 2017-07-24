from staff.models import Member
from datetime import timedelta
import datetime
import kronos
import random

@kronos.register('0 *1/ * * *')
def the_task():
    today = datetime.date.today() #오늘 받기
    Member.objects.filter(end_date__lte=today).update(Membership_status=0)
