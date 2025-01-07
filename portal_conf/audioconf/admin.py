from django.contrib import admin

from .models import AcsPhone, BookingAcs, Department, Employees

admin.site.register(BookingAcs)
admin.site.register(AcsPhone)
admin.site.register(Department)
admin.site.register(Employees)
