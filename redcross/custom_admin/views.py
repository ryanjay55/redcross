from django.shortcuts import render
from account.models import DonorInfo
import xlwt
from django.http import HttpResponse
from datetime import datetime


# Create your views here.
def dashboard(request):
    
    return render(request, 'custom_admin/dashboard.html')

def users(request):
    users = DonorInfo.objects.all()
    return render(request, 'custom_admin/users.html', {'users': users})



def export_donors_info(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="donors.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Donors')

    # Define the column headers
    row_num = 0
    columns = ['ID', 'First Name', 'Last Name', 'Blood Type', 'Date of Birth', 'Email', 'Address', 'Sex', 'Occupation', 'Age', 'Contact Number', 'Completed At','Privacy and Terms Accepted','Consent Accepted']

    # Write column headers in worksheet
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title, font_style)

    # Write donor data in worksheet
    font_style = xlwt.XFStyle()

    rows = DonorInfo.objects.all().values_list('info_id', 'firstname', 'lastname', 'blood_type', 'date_of_birth', 'email', 'address', 'sex', 'occupation', 'age', 'contact_number', 'completed_at','is_privacy_accepted_terms_accepted','is_consent_accepted')
    for row in rows:
        row_num += 1
        for col_num, cell_value in enumerate(row):
            if isinstance(cell_value, datetime):
                cell_value = cell_value.strftime('%d-%m-%Y %H:%M:%S')
            ws.write(row_num, col_num, cell_value, font_style)

    wb.save(response)
    return response
