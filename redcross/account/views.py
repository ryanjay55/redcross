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
            send_registration_email(user)
            messages.success(request, 'Account was created.')
            return redirect('user_login')
        
    context = {'form': form}
    return render(request, 'account/usersignup.html',context)


# METHOD FOR SENDING EMAIL
def send_registration_email(user):
    subject = 'Thank you for completing your profile!'
    message = f'Hi {user.username},\n\nThank you for registering with Lifelink! We appreciate your trust in us and we are committed to providing you with the best service possible.\n\nAccount Information: \n\nemail:{user.email}\n Note: Do not share this to anyone.'
    from_email = 'ryanjayantonio305@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    
def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def completeProfile(request):
    # access_token = 'EAAK00TS0IyEBAHWYoZAnUoLNZB0h8NyMF8XRQPrzlYbxZBnvIT1z8CiG7fs2RztkjETZCbdSgRiEEuJ4RvhED9qjbt1oOviyktcIMm021M2MuhZAvq8fyZBnzuwzGWiscVCapMpjxQT4YDCkvBvZCQf53ZA4LNqifZA7n1OgfWyaszl9H1qgKhgLeug0MWmnxfqvVSqzoHLwadAo26ZC7ZBV7011KvMBYuFephN8LJNEqEdUA8p5AiGZCmqS'
    # response = requests.get(f'https://graph.facebook.com/v12.0/me?fields=email&access_token={access_token}')
    # data = response.json()
    # facebook_email = data['email']
    # Retrieve the current user
    user = request.user

    # Check if the user has already completed their profile
    if DonorInfo.objects.filter(user=user).exists():
        return redirect('dashboard')  # Redirect to dashboard page or any other appropriate page

    # If the request method is POST, process the form submission
    if request.method == 'POST':
        form = CompleteProfileForm(request.POST)
        if form.is_valid():
            # Check if the checkboxes are checked
            checkbox1 = form.cleaned_data.get('is_privacy_accepted_terms_accepted')
            checkbox2 = form.cleaned_data.get('is_consent_accepted')
            if checkbox1 and checkbox2:
                # Create a new DonorInfo object with the form data
                donor_info = form.save(commit=False)
                donor_info.user = user  # Set the user field to the current user
                donor_info.save()
                return redirect('prcusers/dashboard')  # Redirect to dashboard page or any other appropriate page
            else:
                # If checkboxes are not checked, display an error message
                messages.info(request, 'You need to read and accept Privacy Policy and Terms & Conditions and understand how your information will be used.')
                
    else:
        # Set the initial value of the email field to the email of the currently logged in user
        form = CompleteProfileForm(initial={'email': user.email})
        # form = CompleteProfileForm(initial={'email': facebook_email})

    context = {'form': form}
    return render(request, 'account/complete-profile.html', context)

