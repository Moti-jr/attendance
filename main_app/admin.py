from django.contrib import admin

from main_app.models import User,Attendance

# Register your models here.
admin.site.site_header = 'Huduma Attendance'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'auth_user', 'id_number', 'personal_number', 'phone','mda', 'sex', 'date_added')
    search_fields = ('name', 'id_number', 'personal_number', 'phone', 'sex')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date','check_in_time','check_out_time')
    search_fields = ('user__name', 'date')