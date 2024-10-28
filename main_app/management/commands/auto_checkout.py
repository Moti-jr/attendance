from django.core.management.base import BaseCommand
from datetime import datetime

from attendance.main_app.models import Attendance


class Command(BaseCommand):
    help = "Automatically checks out users at 7 PM"

    def handle(self, *args, **kwargs):
        if datetime.now().hour == 19:  # Check if it's 7 PM
            Attendance.objects.filter(checked_out=False).update(
                checked_out=True,
                checked_out_by="system"
            )
            self.stdout.write("Auto checkout complete")