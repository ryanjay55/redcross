from django.shortcuts import render
from inventory.models import BloodBags
from account.models import DonorInfo
import xlwt
from django.core.paginator import Paginator
from django.http import HttpResponse


# Create your views here.


def bloodBagList(request):
    blood_bags = BloodBags.objects.all().order_by('-date_donated')
    paginator = Paginator(blood_bags, 8)  # Show 8 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventory/bloodbaglist.html',{'blood_bags': blood_bags,'page_obj':page_obj})

def bloodInventory(request):
    blood_bags = BloodBags.objects.all().order_by('-date_donated')
    return render(request, 'inventory/inventory.html',{'blood_bags': blood_bags})

import xlwt

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
