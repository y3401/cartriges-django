from bootstrap_modal_forms.generic import BSModalUpdateView
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
#from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.forms.widgets import HiddenInput
from numpy import require
from .models import Cartriges, Printers, Depart, AllPrinters, MetaCart, Sklad, Records, Nmax, MetaCart
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PassRequestMixin

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class CartModelForm(BSModalModelForm):
    class Meta:
        model = Cartriges
        fields = ['name_cart','metacart', 'comment', 'photo']
    def __init__(self, *args, **kwargs):
        super(CartModelForm, self).__init__(*args, **kwargs)
        self.fields['metacart'].queryset = MetaCart.objects.all()

class MetaCartModelForm(BSModalModelForm):
    class Meta:
        model = MetaCart
        fields = ['metatitle']

class PrinterModelForm(BSModalModelForm):
    class Meta:
        model = Printers
        fields = ['name_printer','photo_prn','cart']

class DepartModelForm(BSModalModelForm):
    class Meta:
        model = Depart
        fields = ['name_depart','fio']

class AllPrintersModelForm(BSModalModelForm):
    class Meta:
        model = AllPrinters
        fields = ['inventar_num','printer_model','dep']
#########################################################################################  

class SkladModelForm(BSModalModelForm):
    cartriges = forms.ModelChoiceField(Cartriges.objects.order_by('name_cart'), label="Модель")
    cart_count = forms.IntegerField(min_value=0, label = "Количество на Складе")

    class Meta:
        model = Sklad
        fields = ['cart_buh', 'cartriges', 'cart_count']


class MoveModelForm(BSModalModelForm):
    id_dep = forms.ModelChoiceField(Depart.objects.order_by('name_depart'), label="Передать в ")
    nmax = forms.IntegerField(widget = forms.HiddenInput(), label='') 
    isk = forms.IntegerField(widget = forms.HiddenInput(), label='',required=False) 

    class Meta:
        model = Sklad
        fields = ['cart_buh', 'cartriges', 'cart_count']
        exclude = ['cart_buh',] 
        widgets = {'cartriges': forms.HiddenInput(), 'cart_count' : forms.HiddenInput()}

class Cb0FilterForm(forms.Form):
    cb0= forms.BooleanField(widget= forms.CheckboxInput(), label="")
    
    #class Meta:
    #    fields = ["cb0",]

class RecordsStatusForm(forms.Form):
    isknum = forms.IntegerField(min_value=0, label = "",required=False )
    stat= forms.ChoiceField(choices=Records.LOAN_STATUS, label="",required=False)
    dept= forms.ModelChoiceField(Depart.objects.order_by('name_depart'), label="",required=False)

    class Meta:
        #fields = ['isknum','stat']
        widgets = {"isknum" : forms.CharField()}

    def __init__(self, *args, **kwargs):
        super(RecordsStatusForm, self).__init__(*args, **kwargs)
        #self.fields['used'].choices = [('2', 'Установленные')] + self.fields['used'].choices
        #self.fields['used'].choices = [('1', 'В IT')] + self.fields['used'].choices
        #self.fields['used'].choices = [('0', 'Все')] + self.fields['used'].choices
        self.fields['stat'].choices = [('', '---------')] + self.fields['stat'].choices
        self.fields['dept'].widget.attrs.update({'class': 'w-125px inl_my form-control-my'})
        self.fields['stat'].widget.attrs.update({'class': 'w-125px inl_my form-control-my'})
        self.fields['isknum'].widget.attrs.update({'class': 'w-125px inl_my form-control-my', "placeholder":"Учетный N"})

#########################################################################################    
class RecordsModelForm(BSModalModelForm):
    id_cart = forms.ModelChoiceField(Cartriges.objects.order_by('name_cart'))
    id_dep = forms.ModelChoiceField(Depart.objects.order_by('name_depart'))
    id_cart.label="Модель картриджа"
    id_dep.label="Подразделение"
    nmax = forms.IntegerField(widget = forms.HiddenInput(), label='',required=False)
    
    class Meta:
        model = Records
        fields = ['inventar','id_cart', 'id_dep', 'status', 'charge_num', 'comment'] #'date_out',
        exclude = ['inventar',]
        widgets = {"date_out" : forms.TextInput(attrs = {"type" : "date"}), 
        "charge_num" : forms.NumberInput(attrs = {"type" : "number", "min" : 0})}

