from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .forms import CompleteProfileForm
from django.contrib.auth.decorators import login_required
from .models import DonorInfo
import random



def send_otp(request):
    otp = random.randint(111111,999999)
    email = request.POST.get('email')
    user = DonorInfo.objects.filter(email=email)


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
                return redirect('user-dashboard')
            except DonorInfo.DoesNotExist:
                # Redirect to complete profile page if user does not have complete profile
                return redirect('completeProfile')
        else:
            messages.info(request, 'Username or password is incorrect.')
        
    context = {}
    return render(request, 'account/userlogin.html')


def signupPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            context = {'error': 'Username is already taken'}
            return render(request, 'account/usersignup.html', context)
        
        if password == confirm_password:
            # Create the user object
            user = User.objects.create_user(username=username, email=email, password=password)
            # send_registration_email(user)
            user.save()
            messages.success(request, 'Account was created.')
            return redirect('user_login')
        else:
            # Return an error message if the passwords don't match
            context = {'password_error': 'Passwords do not match'}
            return render(request, 'account/usersignup.html', context)
    else:
        # Render the signup page if the request method is GET
        return render(request, 'account/usersignup.html')



# METHOD FOR SENDING EMAIL
def send_registration_email(user):
    subject = 'Thank you for completing your profile!'
    message = f'Hi {user.username},\n\nThank you for completing your profile in Lifelink, our blood bank management system. Your participation and support are crucial in ensuring a steady supply of safe and adequate blood for patients in need.\n\nWith your updated information, we can keep track of your eligibility to donate blood and provide you with timely notifications on when you can donate again. Your data will also help us match the right blood type to the right patient, ensuring efficient and effective blood transfusions.\n\nAgain, we thank you for your cooperation and support in this noble cause. You are truly making a difference in the lives of many people.\n\nSincerely,\nThe Lifelink Team'
    from_email = 'ryanjayantonio305@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    
def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def completeProfile(request):
    # access_token = 'EAAK00TS0IyEBAM0LPZC9yx0xnZBId2uYeECZBHCwySgIIoyHnSBTtFjRQpxKOIEdNoSSBkR2pZCgx4Ot0O4FZAcHVTVcZC64ToomCBDUSHWPZBBtEtJJj9qAjUwAtDZBQcasp8lWzADMpI01XVwCOG0ODlQXD85u0bpZASgv7hqDiceLdBbZCZBFeSd7xvMPb9ldZCZAldpL5ZAVwHiEw9GmTZCkJt50p69plDp1SNR8HZBT2ZCRzHvC8fFM64WoY'
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
                send_registration_email(user)
                donor_info.save()
                return redirect('user-dashboard')  # Redirect to dashboard page or any other appropriate page
            else:
                # If checkboxes are not checked, display an error message
                messages.info(request, 'You need to read and accept Privacy Policy and Terms & Conditions and understand how your information will be used.')
                
    else:
        # Set the initial value of the email field to the email of the currently logged in user
        form = CompleteProfileForm(initial={'email': user.email})
        # form = CompleteProfileForm(initial={'email': facebook_email})

    return render(request, 'account/complete-profile.html', {'form': form})

