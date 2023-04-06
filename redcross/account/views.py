from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
import requests
from .utils import generate_user_id


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('completeProfile')
        else:
            messages.info(request, 'Username or password is incorrect.')
            # return render(request, 'account/userlogin.html')
        
    context = {}
    return render(request, 'account/userlogin.html')


def signupPage(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Account was created.')
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


def completeProfile(request):
    access_token = 'EAAK00TS0IyEBAIizZApC9ng5SXk3SMaUCg39mJyKFw6honkLwBZC8ZAksMtlTinDffeVYApT2GjGiMVZBkRptI8ZAtdaqF8hxBGD88S2GmdCT3c6WU2IdQsigNa3NpbrM77ZAY9oHZAkyNWzzXNx45RnH5LfllOBy3RkS0FjWUQCowz3dZA3NaUUnnZC3il1EYNkBaVNwJMLZCo7ySVY2tLcvknZBKCkn2my4DiQ0ZA3FSNHTNbIHBUfeTiF'
    # Make a request to the Facebook API to retrieve the user's email address
    response = requests.get(f'https://graph.facebook.com/v12.0/me?fields=email&access_token={access_token}')
    # Parse the response to extract the user's email address
    data = response.json()
    email = data['email']
    
    context = {'email':email}
    return render(request, 'account/complete-profile.html',context)    