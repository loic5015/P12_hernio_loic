from django.contrib import admin
from event.models import Note, Event, Contract, Customer, Company


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'mobile', 'phone', 'date_created', 'date_updated', 'company', 'saler',)

class ContractAdmin(admin.ModelAdmin):
    list_display = ('status', 'amount', 'payement_due', 'date_created', 'date_updated', 'customer', 'saler',)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('note', 'event', 'support', 'customer')

class EventAdmin(admin.ModelAdmin):
    list_display = ('status', 'attendees', 'date_event', 'date_created', 'date_updated', 'customer', 'support', 'contract',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Note, NoteAdmin)

