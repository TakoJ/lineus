from django.contrib import admin
from management.models import *

#FC팀
admin.site.register(FC_Teamleader_Commission)
admin.site.register(FC_Personal_Commission)
admin.site.register(FC_Team_Commission)
#피트니스팀
admin.site.register(Fitness_Teamledaer_Commission)
admin.site.register(Fitness_Personal_Commission)
#필라테스팀
admin.site.register(Pilates_Teamleader_Commission)
admin.site.register(Pilates_Commission)
#필라테스 GX, PT 커미션 정책
admin.site.register(Pilates_GX_Basic)
admin.site.register(Pilates_GX_DependingNum)
admin.site.register(Pilates_PT)
# Register your models here.
