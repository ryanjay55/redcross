from django.shortcuts import render,redirect
# from .forms import SignupForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,permission_required




def index(request):
    return render(request, 'prcuser/index.html')


def home(request):
    context = {'navbar': 'home'}
    return render(request, 'prcuser/index.html', context)


@login_required(login_url='user_logout')
def dashboard(request):
    context = {'request': request}
    return render(request, 'prcuser/dashboard.html',context)

    



