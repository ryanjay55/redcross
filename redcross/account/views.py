from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .forms import CompleteProfileForm
from django.contrib.auth.decorators import login_required
from .models import DonorInfo,OTP
import random



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user_info = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Sorry, we couldn't find an account associated with that email.")
            return render(request, 'account/userlogin.html')

        # Generate a random OTP and store it in a new OTP object associated with the user's User object
        otp = random.randint(100000, 999999)
        try:
            otp_obj = OTP(user=user_info, otp=otp)
            otp_obj.save()
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'account/userlogin.html')
        
        # Send an email to the user's email address containing the OTP
        send_mail(
            'Password reset OTP',
            f'Your OTP is: {otp}',
            'noreply@example.com',
            [email],
            fail_silently=False,
        )
        
        # Redirect the user to a page to enter the OTP they received
        messages.success(request, 'An email with the OTP has been sent to your email address.')
        return render(request, 'account/enter_otp.html', {'email': email})

    # If the request method is not POST, render the forgot_password.html template
    return render(request, 'account/forgot_password.html')



def enter_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_digits = [request.POST.get(f'otp_{i}') for i in range(1, 7)]
        otp_entered = ''.join(otp_digits)
        
        user_info = DonorInfo.objects.filter(email=email).first()
        
        if user_info:
            # Delete expired OTPs
            OTP.objects.filter(user=user_info).delete_if_expired()
            
            # Check if the OTP entered matches the OTP stored in the OTP model for this user
            otp_obj = OTP.objects.filter(user=user_info, otp=otp_entered).first()
            
            if otp_obj:
                # If the OTP is correct, delete the OTP object
                otp_obj.delete()
                
                # Send an email to the user's email address confirming successful OTP verification
                send_mail(
                    'OTP Verification',
                    'Your OTP has been successfully verified.',
                    'noreply@example.com',
                    [email],
                    fail_silently=False,
                )
                
                return render(request, 'account/reset_password.html', {'email': email})
            else:
                messages.error(request, 'Invalid OTP entered.')
                print('Invalid OTP entered')
                return redirect('account/enter_otp.html')  # Redirect back to the forgot password page
        
        messages.error(request, "Sorry, we couldn't find an account associated with that email.")
        print("No account found with the provided email")
        return redirect('account/enter_otp.html')  # Redirect back to the forgot password page
    
    # If the request method is not POST, render the enter_otp.html template with the email that was entered on the forgot password form
    email = request.GET.get('email')
    return render(request, 'account/enter_otp.html', {'email': email})







def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Check if the user has a record in the DonorInfo model 
            try:
                DonorInfo.objects.get(user=user)
                # Redirect to dashboard page if user has complete profile
                messages.success(request, 'Login successful. Let the journey begin.')
                return redirect('user-dashboard')
            except DonorInfo.DoesNotExist:
                # Redirect to complete profile page if user does not have complete profile
                messages.success(request, 'Account verified. Please complete your profile to access all features.')
                return redirect('completeProfile')
        else:
            messages.error(request, 'Username or password is incorrect.')
        
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
        
        # Check if the username length is valid
        if len(username) < 8 or len(username) > 30:
            context = {'password_error1': 'Username must be between 8 and 30 characters long.'}
            return render(request, 'account/usersignup.html', context)
        
         # Check password requirements
        if len(password) < 8 or len(password) > 30:
            context = {'password_error2': 'Password must be between 8 and 30 characters long.'}
            return render(request, 'account/usersignup.html', context)
        
        if not any(char.isdigit() for char in password):
            context = {'password_error2': 'Password must contain at least one digit.'}
            return render(request, 'account/usersignup.html', context)
        
        if not any(char.isalpha() for char in password):
            context = {'password_error2': 'Password must contain at least one letter.'}
            return render(request, 'account/usersignup.html', context)
        
        if not any(char.isupper() for char in password):
            context = {'password_error2': 'Password must contain at least one uppercase letter.'}
            return render(request, 'account/usersignup.html', context)
        
        if not any(char.islower() for char in password):
            context = {'password_error2': 'Password must contain at least one lowercase letter.'}
            return render(request, 'account/usersignup.html', context)
        
        
        if password != confirm_password:
            # Return an error message if the passwords don't match
            context = {'password_error': 'Passwords do not match'}
            return render(request, 'account/usersignup.html', context)
        
        # Create the user object
        user = User.objects.create_user(username=username, email=email, password=password)
        # send_registration_email(user)
        user.save()
        messages.success(request, 'Congratulations! Your account has been successfully created.')
        return redirect('user_login')
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
                messages.warning(request, 'Please read and accept the Privacy Policy and Terms & Conditions, and ensure that you understand how your information will be used.')
                
    else:
        # Set the initial value of the email field to the email of the currently logged in user
        form = CompleteProfileForm(initial={'email': user.email})
        # form = CompleteProfileForm(initial={'email': facebook_email})

    return render(request, 'account/complete-profile.html', {'form': form})

