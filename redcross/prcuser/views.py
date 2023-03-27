from django.shortcuts import render,redirect
from .forms import SignupForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


def index(request):
    return render(request, 'prcuser/index.html')

def home(request):
    return render(request, 'prcuser/index.html')

def dashboard(request):
    return render(request, 'prcuser/dashboard.html')

def loginPage(request):
    if request.method == "POST":
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if the username is an email or a user ID based on the value in tge field
        if request.POST.get('username_type') == 'email':
            user = authenticate(request, email=username, password=password)
        else:
            user = authenticate(request, id=username, password=password)
        # If the user is authenticated, log them in and redirect to the dashboard
        if user is not None:
            login(request, user) 
            return redirect('dashboard')
        else:
            messages.error(request, 'username or password is incorrect')
    
    context = {}
    return render(request, 'prcuser/userlogin.html',context)

        

def signup(request):
    if request.method == "POST":
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            messages.success(request, 'Account registration successful')
            send_registration_email(user)
            return redirect('loginPage')
    else:
        user_form = SignupForm()
    return render(request, 'prcuser/usersignup.html', {'user_form': user_form})

# METHOD FOR SENDING EMAIL
def send_registration_email(user):
    subject = 'Thank you for registering!'
    message = f'Hi {user.firstname},\n\nThank you for registering with Lifelink! We appreciate your trust in us and we are committed to providing you with the best service possible.\n\nAccount Information: \nuser-id: {user.id}\nemail:{user.email}\n Note: Do not share this to anyone.'
    from_email = 'ryanjayantonio305@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
