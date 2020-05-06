from django.contrib import admin
# Register your models here.
from .models import staff,service,servedPatients,order,staffType,bills,MCH,User,Comment

admin.site.register(User)
admin.site.register(staff)
admin.site.register(service)
admin.site.register(servedPatients)
admin.site.register(order)
admin.site.register(staffType)
admin.site.register(bills)
admin.site.register(MCH)
admin.site.register(Comment)

