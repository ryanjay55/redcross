from django.shortcuts import render,HttpResponse
from .forms import SignupForm


# Create your views here.
def index(request):
    return render (request, 'prcuser/index.html')

def home(request):
    return render (request, 'prcuser/index.html')

def login(request):
    return render(request, 'prcuser/userlogin.html')

def signup(request):
    if request.method == "POST":
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse("Registration Successfuly")
    else:
        user_form = SignupForm()
    return render(request, 'prcuser/usersignup.html',{'user_form': user_form})