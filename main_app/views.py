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

@login_required
def check_in(request):
    if request.method == 'POST':
        id_number = request.POST['id_number']
        try:
            user = User.objects.get(id_number=id_number)
            today = timezone.now().date()
            attendance, created = Attendance.objects.get_or_create(user=user, date=today)

            if created:
                attendance.check_in_time = timezone.now()
                attendance.save()
                messages.success(request, f"{user.name}, you have successfully checked in.")
               
            else:
                messages.warning(request, f"{user.name}, you have already checked in for today.")

        except User.DoesNotExist:
            messages.error(request, "The ID number you entered does not exist. Please try again.")

        return redirect('check_in')

    return render(request, 'check_in.html')

@login_required
def check_out(request):
    if request.method == 'POST':
        id_number = request.POST['id_number']
        try:
            user = User.objects.get(id_number=id_number)
            today = timezone.now().date()
            try:
                attendance = Attendance.objects.get(user=user, date=today)
                if attendance.check_out_time is None:
                    attendance.check_out_time = timezone.now()
                    attendance.save()
                    messages.success(request, f"{user.name}, you have successfully checked out.")
                else:
                    messages.warning(request, f"{user.name}, you have already checked out for today.")
            except Attendance.DoesNotExist:
                messages.error(request, f"{user.name}, you have not checked in today. Please check in first.")
                return redirect('check_in')

        except User.DoesNotExist:
            messages.error(request, "The ID number you entered does not exist. Please try again.")

        return redirect('check_out')

    return render(request, 'check_out.html')


def daily_attendance(request):
    today = timezone.now().date()
    attendance_list = Attendance.objects.filter(date=today)
    context = {
        'attendance_list': attendance_list,
    }
    # paginator = Paginator(data, 50)
    # page_number = request.GET.get('page')
    # data = paginator.get_page(page_number)
    # return render(request, 'daily-attendance.html', {'users': data})

#     # if 'download' in request.GET:
#     #     html_string = render_to_string('daily_attendance.html', context)
#     #     html = HTML(string=html_string)
#     #     result = html.write_pdf()

#     #     response = HttpResponse(content_type='application/pdf')
#     #     response['Content-Disposition'] = 'inline; filename=attendance.pdf'
#     #     response.write(result)
#     #     return response

    return render(request, 'daily_attendance.html', context)
