from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import CreateUserForm
from .utils import generate_user_id


def loginPage(request):
    
    return render(request, 'account/userlogin.html')


def signupPage(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # send_registration_email(user)
            return redirect('user_login')
        
    context = {'form': form}
    return render(request, 'account/usersignup.html',context)


# METHOD FOR SENDING EMAIL
def send_registration_email(user):
    subject = 'Thank you for registering!'
    message = f'Hi {user.username},\n\nThank you for registering with Lifelink! We appreciate your trust in us and we are committed to providing you with the best service possible.\n\nAccount Information: \nuser-id: {user.id}\nemail:{user.email}\n Note: Do not share this to anyone.'
    from_email = 'ryanjayantonio305@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    
def user_logout(request):
    logout(request)
    return redirect('user_login')
    