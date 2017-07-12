from django.conf import settings
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from authentication.forms import  StaffRegisterForm

def signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form= SignupForm()
    return render(request, 'signup.html', {
        'form':form,
        })

def staff_register(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management:member_management')
    else:
        form = StaffRegisterForm()

    context = {
        'form' : form
    }
    return render(request, 'staff_register.html', context)


# Create your views here.
