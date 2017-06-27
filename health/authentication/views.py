from django.conf import settings
from django.shortcuts import render,redirect
from authentication.forms import SignupForm
from authentication.models import Profile

def signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form= SignupForm()
    return render(request, 'fitness/signup.html', {
        'form':form,
        })


# Create your views here.
