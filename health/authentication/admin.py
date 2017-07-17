from django.contrib import admin
from .models import User, FC_Salary, Fitness_Salary, Pilates_Salary

admin.site.register(User)
admin.site.register(Fitness_Salary)
admin.site.register(Pilates_Salary)
admin.site.register(FC_Salary)