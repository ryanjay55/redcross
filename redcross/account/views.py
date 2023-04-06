from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import CreateUserForm,CompleteProfileForm
from django.contrib.auth.decorators import login_required
import requests
from .utils import generate_user_id
from .models import DonorInfo


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Check if the user has a record in the DonorInfo model (or the completeProfile model)
            try:
                DonorInfo.objects.get(user=user)
                # Redirect to dashboard page if user has complete profile
                return redirect('dashboard')
            except DonorInfo.DoesNotExist:
                # Redirect to complete profile page if user does not have complete profile
                return redirect('completeProfile')
        else:
            messages.info(request, 'Username or password is incorrect.')
        
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


@login_required
def completeProfile(request):
    # Retrieve the current user
    user = request.user

    # Check if the user has already completed their profile
    if DonorInfo.objects.filter(user=user).exists():
        return redirect('home')  # Redirect to home page or any other appropriate page

    # If the request method is POST, process the form submission
    if request.method == 'POST':
        form = CompleteProfileForm(request.POST)
        if form.is_valid():
            # Create a new DonorInfo object with the form data
            donor_info = form.save(commit=False)
            donor_info.user = user  # Set the user field to the current user
            donor_info.save()
            return redirect('dashboard')  # Redirect to dashboard page or any other appropriate page
    else:
        # Set the initial value of the email field to the email of the currently logged in user
        form = CompleteProfileForm(initial={'email': user.email})

    context = {'form': form}
    return render(request, 'account/complete-profile.html', context)
