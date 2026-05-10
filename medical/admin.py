from django.contrib import admin
from .models import Doctor
from .models import Medicine
from .models import PatientRecord

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'title', 'available_this_week')
    search_fields = ('name', 'department', 'title')



@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'expiry_date', 'created_at')
    search_fields = ('name', 'manufacturer', 'category')
    list_filter = ('category', 'expiry_date')




@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'reason_for_visit', 'time_in', 'time_out', 'attending_doctor', 'created_by')
    list_filter = ('time_in', 'attending_doctor', 'created_by')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'reason_for_visit')
