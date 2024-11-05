from collections import defaultdict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone


from .models import User, Attendance
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
# from weasyprint import HTML
def home(request):
    return render(request, 'index.html')


def check_in(request):
    if request.method == "POST":
        id_number = request.POST.get("id_number")
        try:
            user = User.objects.get(id_number=id_number)
            today = timezone.now().date()

            attendance, created = Attendance.objects.get_or_create(user=user, date=today)

            if created:
                # Save check-in time
                attendance.check_in_time = timezone.now()
                attendance.save()
                messages.success(request, f"{user.name}, Checked in successfully!")
                return render(request, 'check_in.html', {'redirect_after_delay': True})
            else:
                messages.error(request, "You have already checked in today.")
                return render(request, 'check_in.html')

        except User.DoesNotExist:
            messages.error(request, "Invalid ID number.")
            return render(request, 'check_in.html')

    return render(request, 'check_in.html')


def check_out(request):
    if request.method == "POST":
        id_number = request.POST.get("id_number")
        try:
            user = User.objects.get(id_number=id_number)
            today = timezone.now().date()
            attendance = Attendance.objects.filter(user=user, date=today).first()

            if attendance and attendance.check_in_time and not attendance.check_out_time:
                # Save check-out time
                attendance.check_out_time = timezone.now()
                attendance.checked_out_by = "user"  # Manual checkout
                attendance.save()
                messages.success(request, f"{user.name}, checked out successfully!")
                return render(request, 'check_out.html', {'redirect_after_delay': True})
            else:
                messages.error(request, f"{user.name}, you need to check in first or have already checked out.")
        except User.DoesNotExist:
            messages.error(request, "Invalid ID number.")
            return render(request, 'check_out.html')
    return render(request, 'check_out.html')

@login_required(login_url='admin:login')
def daily_attendance(request):
    search_date = request.GET.get('search_date')
    grouped_attendance = {}

    if search_date:
        # Parse the date from the search input
        date_object = timezone.datetime.strptime(search_date, "%Y-%m-%d").date()
    else:
        date_object = timezone.now().date()

    # Fetch attendance records for the specified date
    attendance_records = Attendance.objects.filter(date=date_object)
    if attendance_records.exists():
        grouped_attendance[date_object] = attendance_records

    # Pass the grouped_attendance dictionary and today's date
    return render(request, 'daily_attendance.html', {
        'grouped_attendance': grouped_attendance,
        'today': timezone.now().date(),
    })
# paginator = Paginator(data, 50)
# page_number = request.GET.get('page')
# data = paginator.get_page(page_number)
# return render(request, 'daily-attendance.html', {'users': data})

# if 'download' in request.GET:
#     html_string = render_to_string('daily_attendance.html', context)
#     html = HTML(string=html_string)
#     result = html.write_pdf()

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename=attendance.pdf'
#     response.write(result)
#     return response
