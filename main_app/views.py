import datetime
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
            # attendance,created =Attendance.objects.get_or_create(user=user,date=today)
            # Define the 8:30 AM cutoff time

            # cutoff_time = now.replace(8, 30,00 )  # 08:30:00
            #
            # if now > cutoff_time:
            #     messages.error(request, "You cannot check in after 8:30 AM.")
            #     return redirect('check_in')

            attendance, created = Attendance.objects.get_or_create(user=user, date=today)

            if created:
                # Save check-in time
                attendance.check_in_time = timezone.now()
                attendance.save()
                messages.success(request, f"{user.name}, Checked in successfully!")
            else:
                messages.error(request, "You have already checked in today.")
        except User.DoesNotExist:
            messages.error(request, "Invalid ID number.")

        # Clear the ID input after submission
        return redirect('check_in')

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
                attendance.save()
                messages.success(request, f"{user.name},Checked out successfully!")
            else:
                messages.error(request, f"{user.name},You need to check in first or have already checked out.")
        except User.DoesNotExist:
            messages.error(request, "Invalid ID number.")

        # Clear the ID input after submission
        return redirect('home')

    return render(request, 'check_out.html')

@ login_required(login_url='admin:login')
def daily_attendance(request):
    # Fetch all attendance records ordered by date (latest first)
    attendance_records = Attendance.objects.all().order_by('-date')

    # Group attendance records by date
    grouped_attendance = defaultdict(list)
    daily_totals = defaultdict(int)  # Keep track of the total check-ins for each day
    today = timezone.now().date()
    total_checked_in_today = 0

    for attendance in attendance_records:
        # Group attendances by date
        grouped_attendance[attendance.date].append(attendance)

        # Count total check-ins for each day
        if attendance.check_in_time is not None:
            daily_totals[attendance.date] += 1

        # Count the number of people who checked in today
        if attendance.date == today and attendance.check_in_time is not None:
            total_checked_in_today += 1

    # Sort the grouped attendance by date in reverse order (latest date first)
    grouped_attendance = dict(sorted(grouped_attendance.items(), reverse=True))

    context = {
        'grouped_attendance': grouped_attendance,
        'total_checked_in_today': total_checked_in_today,
        'daily_totals': daily_totals,  # Pass the daily totals to the template
        'today': today  # Pass the `today` variable to the template
    }

    return render(request, 'daily_attendance.html', context)

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
