from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Tour)

admin.site.register(Ticket)
admin.site.register(Location)
admin.site.register(TransportCompany)
admin.site.register(TransportPrice)
admin.site.register(Review)
admin.site.register(TransactionTx)