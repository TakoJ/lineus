from django.core.management.base import BaseCommand, CommandError
from staff.models import Member
from datetime import timedelta
import datetime

class Command(BaseCommand):

    args = ''

    def handle(self, *args, **options):

        today = datetime.date.today() #오늘
        Member.objects.filter(end_date__lt=today).update(Membership_status=0)