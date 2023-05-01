from django.shortcuts import render,redirect
from django.core.mail import send_mail
from account.models import DonorInfo
from inventory.models import BloodBags
import xlwt
from django.http import HttpResponse
from datetime import datetime
from xlwt import easyxf
from django.core.paginator import Paginator
from django.db.models.functions import ExtractYear,Concat
from django.db.models import Value, CharField,Count, Max,F,ExpressionWrapper, IntegerField




# Create your views here.
def dashboard(request):
    
    return render(request, 'custom_admin/dashboard.html',{'sidebar':dashboard})

from datetime import datetime

from datetime import datetime

def usersList(request):
    # if request.method == 'POST':
    #     # Retrieve the form data
    #     info_id = request.POST.get('info_id')
    #     firstname = request.POST.get('firstname')
    #     lastname = request.POST.get('lastname')
    #     sex = request.POST.get('sex')
    #     blood_type = request.POST.get('blood_type')

    #     email = request.POST.get('email')
    #     address = request.POST.get('address')
    #     contact_number = request.POST.get('contact_number')

    #     # Convert date_of_birth string to datetime object

  

    #     # Retrieve the existing DonorInfo object
    #     donor_info = DonorInfo.objects.get(info_id=info_id)

    #     # Update the DonorInfo object with the form data
    #     donor_info.firstname = firstname
    #     donor_info.lastname = lastname
    #     donor_info.sex = sex
    #     donor_info.blood_type = blood_type
  
    #     donor_info.email = email
    #     donor_info.address = address
    #     donor_info.contact_number = contact_number

    #     # Save the updated DonorInfo object to the database
    #     donor_info.save()

    #     # Redirect to the users list page
    #     return redirect('users-list')
    
    donors = DonorInfo.objects.all()
    serial_exists_error = ''
    serial_incomplete_error = ''
    submission_success = ''

    if request.method == 'POST':
        # Handle the modal form data here
        info_id = request.POST.get('info_id')
        serial_no_1 = request.POST.get('serial_no_1')
        serial_no_2 = request.POST.get('serial_no_2')
        serial_no_3 = request.POST.get('serial_no_3')
        serial_no = serial_no_1 + '-' + serial_no_2 + '-' + serial_no_3
        date_donated = request.POST.get('date_donated')
        bled_by = request.POST.get('bled_by')


        # Validate the serial number
        if len(serial_no_1) != 4 or len(serial_no_2) != 6 or len(serial_no_3) != 1:
            serial_incomplete_error = 'Serial number must have the format XXXX-XXXXXX-X.'
        elif BloodBags.objects.filter(serial_no=serial_no).exists():
            serial_exists_error = 'Serial number already exists in the database.'

        # Check if DonorInfo record with id exists in database
        try:
            donor_info = DonorInfo.objects.get(pk=info_id)
        except DonorInfo.DoesNotExist:
            # Return an error message if the record does not exist
            return HttpResponse('Error: DonorInfo record with id {} does not exist'.format(info_id))

        else:
            if not serial_exists_error and not serial_incomplete_error:
                # Create a new BloodBags instance based on the form data and DonorInfo record
                blood_bag = BloodBags(
                    info_id=donor_info,
                    serial_no=serial_no,
                    date_donated=date_donated,
                    bled_by=bled_by,
                )
                blood_bag.save()
                submission_success = 'Blood bag successfully added to the database.'

        
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
    return render(request, 'custom_admin/users.html', {'users': page_obj, 'sidebar': page_obj, 'modal': True, 'rows': rows,'donors':donors,'serial_exists_error':serial_exists_error,'donors': donors,'serial_incomplete_error': serial_incomplete_error,'submission_success':submission_success})


def send_thank_you_email(donor_info):
    subject = 'Thank you for donating blood'
    message = f'Hi {donor_info.firstname} {donor_info.lastname},\n\nWe want to express our sincerest thanks for taking the time and effort to donate blood at our blood donation event. Your selfless act of donating blood has the potential to save lives and make a significant difference in the lives of those in need.\n\nYour donation will be used to help patients who are undergoing surgery, experiencing medical emergencies, or undergoing treatment for life-threatening conditions. Your generosity and willingness to give back to your community is truly appreciated.\n\nWe also want to acknowledge the courage and strength it takes to donate blood. We understand that some people may be nervous or anxious about the process, and we thank you for overcoming any fears or discomfort in order to make a difference in the lives of others.\n\nOnce again, thank you for your donation and for being a part of our blood donation community. We hope that you will continue to support our efforts in the future. \n\n\nSincerely,\n\nRed Cross Valenzuela City Chapter \nLifeLink'
    from_email = 'ryanjayantonio305@gmail.com'
    recipient_list = [donor_info.email]
    send_mail(subject, message, from_email, recipient_list)


def donorList(request):
    sort_param = request.GET.get('sort', '-last_donation')  # default sort by last donation date in descending order
    blood_bags = BloodBags.objects.select_related('info_id').annotate(
        age=ExpressionWrapper(
            datetime.now().year - ExtractYear(F('info_id__date_of_birth')),
            output_field=IntegerField()
        ),
        full_name=Concat('info_id__firstname', Value(' '), 'info_id__lastname', output_field=CharField())
    ).values(
        'info_id', 'full_name', 'age', 'info_id__blood_type', 'info_id__date_of_birth', 'info_id__email',
        'info_id__sex', 'info_id__contact_number', 'info_id__address', 'info_id__occupation', 'info_id__completed_at'
    ).annotate(
        num_donations=Count('bag_id'),
        last_donation=Max('date_donated')
    )
    
    if sort_param == 'name':
        blood_bags = blood_bags.order_by('full_name')
    elif sort_param == 'bloodtype':
        blood_bags = blood_bags.order_by('info_id__blood_type')
    elif sort_param == 'num_donations':
        blood_bags = blood_bags.order_by('-num_donations')
    elif sort_param == 'sex':
        blood_bags = blood_bags.order_by('info_id__sex')
    elif sort_param == 'age':
        blood_bags = blood_bags.order_by('age')
    else:
        blood_bags = blood_bags.order_by('-info_id__completed_at')

    paginator = Paginator(blood_bags, 8)  # Show 8 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'custom_admin/donorlist.html', {'blood_bags': blood_bags, 'page_obj': page_obj})






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

