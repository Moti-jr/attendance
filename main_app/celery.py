from django.db.models.functions import datetime
from .models import Attendance


@shared_task
def automatic_checkout():
    # Get current time and compare
    if datetime.now().hour == 19:  # 7 PM in 24-hour format
        Attendance.objects.filter(checked_out=False).update(
            checked_out=True,
            checked_out_by="system"
        )