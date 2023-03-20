from django.shortcuts import render

# Create your views here.
def index(request):
    return render (request, 'prcuser/index.html')

def home(request):
    return render (request, 'prcuser/index.html')

def login(request):
    return render(request, 'prcuser/userlogin.html')

def signup(request):
    return render(request, 'prcuser/usersignup.html')