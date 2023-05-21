from django.shortcuts import render
from inventory.models import BloodBags,BloodInventory,ExpiredBlood
from account.models import DonorInfo
import xlwt
from django.core.paginator import Paginator
from django.db.models.functions import Concat
from django.db.models import Value, CharField
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta,date



def bloodBagList(request):
    
    now = datetime.now()
    blood_bags = BloodBags.objects.all().order_by('-date_donated')
    full_name = Concat('info_id__firstname', Value(' '), 'info_id__lastname', output_field=CharField())

    sort_param = request.GET.get('sort', '-date_donated')  # default sort by date_donated in descending order
    if sort_param == 'full_name':
        blood_bags = blood_bags.annotate(donor_name=full_name).order_by('donor_name')
    elif sort_param == '-full_name':
        blood_bags = blood_bags.annotate(donor_name=full_name).order_by('-donor_name')
    elif sort_param == 'blood_type':
        blood_bags = blood_bags.order_by('info_id__blood_type')
    elif sort_param == '-blood_type':
        blood_bags = blood_bags.order_by('-info_id__blood_type')

    paginator = Paginator(blood_bags, 7)  # Show 7 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Pass the current parameter value to the pagination links
    if sort_param == 'full_name':
        page_obj.sort_param = '&sort=full_name'
    elif sort_param == '-full_name':
        page_obj.sort_param = '&sort=-full_name'
    elif sort_param == 'info_id__blood_type':
        page_obj.sort_param = '&sort=blood_type'
    elif sort_param == '-info_id__blood_type':
        page_obj.sort_param = '&sort=-blood_type'
        
    # Pass the current sort parameter value to the next and previous page links
    if page_obj.has_previous():
        page_obj.previous_page_number_param = f'&sort={sort_param}&page={page_obj.previous_page_number()}'
    if page_obj.has_next():
        page_obj.next_page_number_param = f'&sort={sort_param}&page={page_obj.next_page_number()}'
    return render(request, 'inventory/bloodbaglist.html',{'blood_bags': blood_bags,'page_obj': page_obj,'now':now,'navbar': 'bloodBagList'})


def bloodInventory(request):
    blood_type = request.GET.get('blood_type', 'A+')
    bags = BloodBags.objects.filter(info_id__blood_type=blood_type)
    blood_inventory = BloodInventory.objects.filter(bag_id__info_id__blood_type=blood_type).order_by('exp_date')
    expired_blood = ExpiredBlood.objects.filter(bag_id__info_id__blood_type=blood_type).order_by('exp_date')
    stock_count = blood_inventory.count()
    expired_count = expired_blood.count()

    now = timezone.now()
    high_priority_threshold = now + timedelta(days=7)
    medium_priority_threshold = now + timedelta(days=14)
    low_priority_threshold = now + timedelta(days=42)

    if request.method == 'POST':
        serial_no = request.POST.get('serial_no')

        try:
            blood_bag = BloodBags.objects.get(serial_no=serial_no)

            if BloodInventory.objects.filter(bag_id=blood_bag).exists():
                error_message = 'Serial number {} already exists in the BloodInventory.'.format(serial_no)
                messages.error(request, error_message)
            elif ExpiredBlood.objects.filter(bag_id=blood_bag).exists():
                error_message = 'Serial number {} already exists in the ExpiredBlood table.'.format(serial_no)
                messages.error(request, error_message)
            else:
                exp_date = blood_bag.get_exp_date().date()  # Convert datetime.datetime to datetime.date

                if exp_date <= date.today():
                    expired_blood_obj = ExpiredBlood.objects.create(bag_id=blood_bag, exp_date=exp_date)
                    expired_count += 1
                    error_message = 'Blood bag with serial number {} has expired and will be added to the Expired Blood List.'.format(serial_no)
                    messages.success(request, error_message)
                else:
                    blood_inventory_obj = BloodInventory.objects.create(bag_id=blood_bag, exp_date=exp_date)
                    stock_count += 1
                    success_message = 'Blood bag with serial number {} has been added to the BloodInventory.'.format(serial_no)
                    messages.success(request, success_message)

        except BloodBags.DoesNotExist:
            error_message = 'Blood bag with serial number {} does not exist.'.format(serial_no)
            messages.error(request, error_message)

    # Move expired blood from BloodInventory to ExpiredBlood
    expired_blood_to_move = blood_inventory.filter(exp_date__lte=date.today())
    for expired_blood_obj in expired_blood_to_move:
        ExpiredBlood.objects.create(bag_id=expired_blood_obj.bag_id, exp_date=expired_blood_obj.exp_date)
        expired_blood_obj.delete()
        # stock_count -= 1
        # expired_count += 1

    priority_mapping = {
        'high': high_priority_threshold,
        'medium': medium_priority_threshold,
        'low': low_priority_threshold
    }

    blood_inventory_with_priority = []
    for item in blood_inventory:
        exp_datetime = item.exp_date
        priority = 'low'  # Default priority is low
        if exp_datetime <= high_priority_threshold:
            priority = 'high'
        elif exp_datetime <= medium_priority_threshold:
            priority = 'medium'
        blood_inventory_with_priority.append((item, priority))

    return render(request, 'inventory/inventory.html', {'now': now, 'bags': bags, 'blood_inventory_with_priority': blood_inventory_with_priority, 'stock_count': stock_count, 'priority_mapping': priority_mapping,'navbar': 'bloodInventory'})


    
    
def expiredBlood(request):
    expired_blood = ExpiredBlood.objects.all()  # Retrieve all expired blood objects
    expired_count = expired_blood.count()  # Count the number of expired blood objects

    return render(request, 'inventory/expiredblood.html', {'expired_blood': expired_blood,'expired_count':expired_count,'navbar': 'expiredBlood'})





def exportBloodBagList_to_xls():
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="donors.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Donors')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Info ID', 'Name', 'Serial Number', 'Blood Type', 'Date Donated', 'Bled By']

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title, font_style)

    font_style = xlwt.XFStyle()

    rows = DonorInfo.objects.values_list('info_id', 'firstname', 'lastname', 'blood_type', 'blooddonation__date_donated', 'blooddonation__bled_by__username').order_by('-blooddonation__date_donated')

    for row in rows:
        row_num += 1
        for col_num, cell_value in enumerate(row):
            if col_num == 1:
                cell_value = f'{row[1]} {row[2]}'
            ws.write(row_num, col_num, cell_value, font_style)

    wb.save(response)
    return response
