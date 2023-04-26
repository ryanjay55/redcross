from django.shortcuts import render,redirect
from account.models import DonorInfo
from inventory.models import BloodBags
import xlwt
from django.http import HttpResponse
from datetime import datetime
from xlwt import easyxf
from django.core.paginator import Paginator
from django.db.models import F
from django.db.models.functions import ExtractYear


# Create your views here.
def dashboard(request):
    
    return render(request, 'custom_admin/dashboard.html',{'sidebar':dashboard})

def usersList(request):
    donors = DonorInfo.objects.all()
    serial_exists_error = ''
    if request.method == 'POST':
        # Handle the modal form data here
        info_id = request.POST.get('info_id')
        serial_no = request.POST.get('serial_no')
        date_donated = request.POST.get('date_donated')
        bled_by = request.POST.get('bled_by')

        if not info_id:
            # Return an error message if info_id is empty or None
            return HttpResponse('Error: DonorInfo record id is required')

        # Check if DonorInfo record with id exists in database
        try:
            donor_info = DonorInfo.objects.get(pk=info_id)
        except DonorInfo.DoesNotExist:
            # Return an error message if the record does not exist
            return HttpResponse('Error: DonorInfo record with id {} does not exist'.format(info_id))

        # Check if the entered serial number already exists in the database
        if BloodBags.objects.filter(serial_no=serial_no).exists():
            serial_exists_error = 'Serial number already exists.'

        # Create a new BloodBags instance based on the form data and DonorInfo record
        blood_bag = BloodBags(
            info_id=donor_info,
            serial_no=serial_no,
            date_donated=date_donated,
            bled_by=bled_by,
        )
        blood_bag.save()
        
    sort_param = request.GET.get('sort', 'completed_at')  # default sort by completion date
    if sort_param == 'firstname':
        user_list = DonorInfo.objects.order_by('firstname')
    elif sort_param == 'blood_type':
        user_list = DonorInfo.objects.order_by('blood_type')
    elif sort_param == 'sex':
        user_list = DonorInfo.objects.order_by('sex')
    elif sort_param == 'age_asc':
        user_list = DonorInfo.objects.annotate(
            computed_age=ExtractYear(F('completed_at')) - ExtractYear(F('date_of_birth'))
        ).order_by('age')
    else:
        user_list = DonorInfo.objects.order_by('-completed_at')
    paginator = Paginator(user_list, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Pass the current sort parameter value to the pagination links
    if sort_param == 'firstname':
        page_obj.sort_param = '&sort=firstname'
    elif sort_param == 'blood_type':
        page_obj.sort_param = '&sort=blood_type'
    elif sort_param == 'sex':
        page_obj.sort_param = '&sort=sex'
    elif sort_param == 'age_asc':
        page_obj.sort_param = '&sort=age_asc'
    else:
        page_obj.sort_param = ''
    # Pass the current sort parameter value to the next and previous page links
    if page_obj.has_previous():
        page_obj.previous_page_number_param = f'&sort={sort_param}&page={page_obj.previous_page_number()}'
    if page_obj.has_next():
        page_obj.next_page_number_param = f'&sort={sort_param}&page={page_obj.next_page_number()}'
    rows = [{'id': user.pk, 'firstname': user.firstname, 'lastname': user.lastname} for user in page_obj]
    return render(request, 'custom_admin/users.html', {'users': page_obj, 'sidebar': page_obj, 'modal': True, 'rows': rows,'donors':donors,'serial_exists_error':serial_exists_error})


def donorList(request):
    return render(request, 'custom_admin/donorlist.html')

def bloodBagList(request):
    return render(request, 'custom_admin/bloodbaglist.html')

def export_donors_info(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="UserList.xls"'

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

    # Define custom date format
    date_format = easyxf(num_format_str='MMMM DD, YYYY')

    rows = DonorInfo.objects.all().values_list('info_id', 'firstname', 'lastname', 'blood_type', 'date_of_birth', 'email', 'address', 'sex', 'occupation', 'age', 'contact_number', 'completed_at','is_privacy_accepted_terms_accepted','is_consent_accepted')
    for row in rows:
        row_num += 1
        for col_num, cell_value in enumerate(row):
            if col_num == 4: # If the column is Date of Birth
                cell_value = datetime.strptime(str(cell_value), '%Y-%m-%d').date()
                ws.write(row_num, col_num, cell_value, date_format)
            elif isinstance(cell_value, datetime):
                cell_value = cell_value.strftime('%d-%m-%Y %H:%M:%S')
                ws.write(row_num, col_num, cell_value, font_style)
            else:
                ws.write(row_num, col_num, cell_value, font_style)

    wb.save(response)
    return response

