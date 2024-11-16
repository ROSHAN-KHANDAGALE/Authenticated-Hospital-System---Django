from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PatientRegister)
admin.site.register(DoctorRegister)
admin.site.register(DoctorList)
admin.site.register(DateBooking)
admin.site.register(SlotBooking)
admin.site.register(Appointees)
admin.site.register(ContactUser)
admin.site.register(Medication)
admin.site.register(SuggestedMedicine)
admin.site.register(User)
admin.site.register(ResetUuid)
