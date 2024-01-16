from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(SystemUsers)
admin.site.register(Appointmentt)

admin.site.register(TimeSlot)
admin.site.register(NewAppointmentt)
admin.site.register(NewTemporaryAppointment)
admin.site.register(NewTimeSlot)
admin.site.register(Ex)
admin.site.register(TemporarySecond)
admin.site.register(AppointmentSecond)
admin.site.register(TimeSlotSecond)