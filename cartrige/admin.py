from django.contrib import admin
from .models import (
    Cartriges, 
    Records, 
    Printers, 
    Sklad,
    Depart, 
    Nmax, 
    AllPrinters,
    MetaCart,
    ContrAgent,
    Logs,
    Operation)

admin.site.register(Nmax)
#admin.site.register(MetaCart)

@admin.register(Operation)
# Define the admin class                        OPERATION
class OperationAdmin(admin.ModelAdmin):
    list_display = ('kod', 'operation_name')
    fields = ['kod','operation_name']

@admin.register(Logs)
# Define the admin class                        LOGS
class LogsAdmin(admin.ModelAdmin):
    list_display = ('date_event', 'name_user','action','obj','izm')
    fields = ['name_user','action','obj','izm']

@admin.register(Depart)
# Define the admin class                        DEPART
class DepartAdmin(admin.ModelAdmin):
    list_display = ('name_depart', 'fio','adm')
    fields = ['name_depart', 'fio','adm']

@admin.register(ContrAgent)
# Define the admin class                        CONTRAGENT
class ContrAgentAdmin(admin.ModelAdmin):
    list_display = ['name_agent', 'name_agent_full', 'fio_nach', 'nach_dolj', 'fio_zam', 'email', 'phone', 'otvet', 'inn', 'address', 'adm']
    fields = ['name_agent', 'name_agent_full', ('nach_dolj','fio_nach', 'fio_zam'), ('inn', 'address', 'email', 'phone'), 'otvet',  'adm']

@admin.register(Printers)
# Define the admin class                        PRINTERS
class PrintersAdmin(admin.ModelAdmin):
    list_display = ('name_printer', 'photo_prn')
    fields = ['name_printer', 'photo_prn', 'cart']
    

class PrinterInline(admin.TabularInline):
    model = Printers.cart.through
    extra = 0

#class CartrigesInline(admin.TabularInline):
#    model = Cartriges
#    extra = 0
    #fields = ['name_cart']
#    can_delete = False
    #list_display = ['name_cart']
    #prepopulated_fields = {'name_cart':('name_cart',)}
    
@admin.register(MetaCart)
# Define the admin class                        METACART
class MetaCartAdmin(admin.ModelAdmin):
    list_display = ('metatitle',)
    fields = ['metatitle',]
#    inlines = [CartrigesInline]



@admin.register(Cartriges)
# Define the admin class                        CARTRIGES
class CartrigesAdmin(admin.ModelAdmin):
    list_display = ('name_cart','metacart', 'photo', 'comment')
    fields = [('name_cart','metacart'), 'photo', 'comment']
    inlines = [PrinterInline]


@admin.register(Sklad)
# Define the admin class                        SKLAD
class SkladAdmin(admin.ModelAdmin):
    list_display = ('cartriges', 'cart_buh', 'cart_count')
    fields = ['cartriges', 'cart_buh', 'cart_count']

@admin.register(AllPrinters)
# Define the admin class                        ALLPRINTERS
class AllPrintersAdmin(admin.ModelAdmin):
    list_display = ('inventar_num', 'printer_model', 'dep')
    fields = ['inventar_num', 'printer_model', 'dep']

@admin.register(Records)
# Define the admin class                        RECORDS
class SkladAdmin(admin.ModelAdmin):
    list_display = ('inventar', 'id_cart', 'id_dep', 'status', 'date_in', 'date_out','charge_num','c_agent')
    fields = ['inventar', 'id_cart', 'id_dep', 'status', 'date_in', 'date_out','charge_num', 'comment']



