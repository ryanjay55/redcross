from django.shortcuts import render
from inventory.models import BloodBags
from account.models import DonorInfo
import xlwt
from django.core.paginator import Paginator
from django.db.models.functions import ExtractYear,Concat,ExtractMonth
from django.db.models import Value, CharField,Count, Max,F,ExpressionWrapper, IntegerField
from django.http import HttpResponse
import xlwt
from datetime import datetime



# Create your views here.


def bloodInventory(request):
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
        
    now = datetime.now()    
        
    return render(request, 'inventory/inventory.html',{'blood_bags': blood_bags,'page_obj': page_obj,'now':now})


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
