from django.shortcuts import render, redirect
from django.utils import timezone
from account.models import DonorInfo
from inventory.models import BloodBags
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
import datetime



def index(request):
    return render(request, 'prcuser/index.html')


def home(request):
    context = {'navbar': 'home'}
    return render(request, 'prcuser/index.html', context)


@login_required(login_url='user_login')
def dashboard(request):
    user = request.user
    # print('Current user:', user)
    donated_blood_count = BloodBags.objects.filter(info_id__user=user).count()
    # print('Donated blood count:', donated_blood_count)
    blood_types = DonorInfo.objects.values_list('blood_type', flat=True).distinct()
    available_blood_types = request.session.get('available_blood_types', {blood_type: False for blood_type in blood_types})

    return render(request, 'prcuser/dashboard.html', {'navbar': 'dashboard', 'donated_blood_count': donated_blood_count, 'available_blood_types': available_blood_types})

@login_required(login_url='user_login')
def bloodJourney(request):
    return render(request, 'prcuser/bloodjourney.html')

@login_required(login_url='user_login')
def donationHistory(request):
    user = request.user
    donor_info = DonorInfo.objects.get(user=user)
    blood_bags = BloodBags.objects.filter(info_id__user_id=user.id).order_by('-date_donated')

    # Calculate the days since the most recent donation
    days_since_last_donation = None
    if blood_bags:
        most_recent_donation = blood_bags[0]
        time_since_donation = timezone.now() - make_aware(datetime.datetime.combine(most_recent_donation.date_donated, datetime.time()))
        days_since_last_donation = time_since_donation.days - 1

    no_donations = False
    if not blood_bags:
        no_donations = True

    return render(request, 'prcuser/donationHistory.html', {'blood_bags': blood_bags, 'days_since_last_donation': days_since_last_donation, 'no_donations': no_donations})




@login_required(login_url='user_login')
def bloodDonorNetowrk(request):
    return render(request, 'prcuser/blooddonornetwork.html')

@login_required(login_url='user_login')
def profile(request):
    return render(request, 'prcuser/profile.html')


