from typing import Any, Dict
from bootstrap_modal_forms.forms import BSModalForm
from django import forms
from django.core.checks.messages import Debug
from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.db.models.query import Prefetch
from django.shortcuts import redirect, render
from django.urls.base import set_urlconf
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F,Count
from django.template import RequestContext
from .models import (Cartriges, ContrAgent, Depart, Printers, AllPrinters, Sklad, Records, Nmax, Logs, Operation, Tmp, MetaCart)
from django.views import generic
import datetime
from django.utils import timezone
from django.db import connection
from django.db import models
import random


sfq= '''SELECT 1 as id ,metatitle, name_cart, count(*) as cou,status FROM 
(SELECT cm.metatitle, cc.name_cart, cr.status 
FROM cartrige_records AS cr, cartrige_cartriges AS cc, cartrige_metacart AS cm WHERE cr.id_cart_id=cc.id AND cc.metacart_id=cm.id) as tmp  
GROUP BY metatitle,status,name_cart 
ORDER BY metatitle,status,name_cart
'''
sfq_1 = '''SELECT 1 as id,name_cart,cart_count FROM cartrige_sklad AS cs,cartrige_cartriges AS cc WHERE cs.cartriges_id= cc.id AND cs.cart_count > 0 ORDER BY name_cart;'''

def index(request):
    all_records = Records.objects.raw(sfq) #aggregate(Count('id_cart__name_cart')).values('status')  # Метод 'all()' применён по умолчанию.
    ost_sklad = Sklad.objects.raw(sfq_1)
    num_rec = Records.objects.count()
    inwork = Records.objects.filter(status=2).count()
    inreserve = Records.objects.filter(status__in = {1,5}).count()
    isempty = Records.objects.filter(status=3).count()
    isload = Records.objects.filter(status=4).count()

    return render(
        request,
        'index.html',
        context={'all_records': all_records, 'ost_sklad': ost_sklad, 'num_rec' : num_rec, 'inwork' : inwork, 'inreserve' : inreserve, 'isempty' : isempty, 'isload' : isload},
    )

def Logging(t,u,a,ob,izm=""):      # запись в лог
    dt = datetime.datetime.today() #.strftime("%d.%m.%Y %H:%M:%S") #timezone.now() #
    sfq='INSERT INTO cartrige_logs(date_event,token,name_user,action_id,obj,izm) VALUES (%s, %s, %s, %s, %s, %s);'
    with connection.cursor() as cursor:
        cursor.execute(sfq,[dt,t,u,a,ob,izm])

def createToken():
    lower="abcdefghijklmnopqrstuwvxyz"
    upper=lower.upper()
    digit="0123456789"
    all=lower+upper+digit
    length=32
    token= "".join(random.sample(all,length))
    return token


def stat():
    all_records = Records.objects.raw(sfq) #aggregate(Count('id_cart__name_cart')).values('status')  # Метод 'all()' применён по умолчанию.
    ost_sklad = Sklad.objects.raw(sfq_1)
    num_rec = Records.objects.count()
    inwork = Records.objects.filter(status=2).count()
    inreserve = Records.objects.filter(status__in = {1,5}).count()
    isempty = Records.objects.filter(status=3).count()
    isload = Records.objects.filter(status=4).count()
    data={}
    data['all_records'] = all_records
    data['ost_sklad'] = ost_sklad
    data['num_rec'] = num_rec
    data['inwork'] = inwork
    data['inreserve'] = inreserve
    data['isempty'] = isempty
    data['isload'] = isload
    return data


from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, request
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import (
    BSModalFormView,
    BSModalReadView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalDeleteView)
from .forms import (
    CartModelForm,
    PrinterModelForm, 
    DepartModelForm, 
    AllPrintersModelForm,
    SkladModelForm,
    RecordsModelForm,
    MoveModelForm,
    RecordsStatusForm,
    MetaCartModelForm) 
#    CustomAuthenticationForm)

def NMax():
    try:
        for inv in Nmax.objects.raw("SELECT * FROM cartrige_nmax WHERE zapis=0"):
            n_max = inv.nmax + 1
    except:
        for inv in Nmax.objects.raw("SELECT * FROM cartrige_nmax WHERE zapis=0"):
            n_max = inv.nmax
    return n_max


''' Вьюшки для справочника картриджей'''
#@permission_required('cartriges.can_mark_returned')

class CartrigeListView(LoginRequiredMixin,generic.ListView):
    model = Cartriges
    paginate_by = 5
    #paginate_orphans = 2

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data1 = stat()
        data = super().get_context_data(**kwargs)
        data['all_records'] = data1['all_records']
        data['ost_sklad'] = data1['ost_sklad']
        data['num_rec'] = data1['num_rec']
        data['inwork'] = data1['inwork']
        data['inreserve'] = data1['inreserve']
        data['isempty'] = data1['isempty']
        data['isload'] = data1['isload']

        try:
            page=self.request.GET['page']
        except:
            page=1
        data['pn'] = page     
        return data

class CartrigeDetailView(LoginRequiredMixin,generic.DetailView):
    model = Cartriges

class CartCreateView(LoginRequiredMixin,BSModalCreateView):
    template_name = 'cartrige/cartriges_form.html'
    form_class = CartModelForm
    success_url = reverse_lazy('cartriges-list')

class CartrigeUpdate(LoginRequiredMixin, BSModalUpdateView):
    model = Cartriges
    template_name = 'cartrige/cartriges_form.html'
    form_class = CartModelForm
    
    def get_success_url(self) -> str:
        try:
            pn=self.request.GET['page']
        except:
            pn=1
        return (reverse_lazy('cartriges-list')) + '?page='+ str(pn)


class CartrigeDelete(LoginRequiredMixin, BSModalDeleteView):
    model = Cartriges
    success_message = ''

    def get_success_url(self) -> str:
        return reverse_lazy('cartriges-list')
    
    def delete(self,request, *args, **kwargs):
        try:
            rend = super(CartrigeDelete, self).delete(request, *args, **kwargs)
            if rend:
                messages.success(request,"Удалено!")
            return rend
        except models.ProtectedError as e:
            success_message = ""
            try:
                pn = self.request.GET['page']
            except:
                pn = 1
            messages.success(request,"Эта модель картриджа задействована! Удалить невозможно!")
            return HttpResponseRedirect((reverse('cartriges-list')) + '?page='+ str(pn))

''' Вьюшки для справочника принтеров'''
#@permission_required('printers.can_mark_returned')
class PrinterListView(LoginRequiredMixin,generic.ListView):
    model = Printers
    paginate_by = 5

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data1 = stat()
        data = super().get_context_data(**kwargs)
        data['all_records'] = data1['all_records']
        data['ost_sklad'] = data1['ost_sklad']
        data['num_rec'] = data1['num_rec']
        data['inwork'] = data1['inwork']
        data['inreserve'] = data1['inreserve']
        data['isempty'] = data1['isempty']
        data['isload'] = data1['isload']
        try:
            page=self.request.GET['page']
        except:
            page=1
        data['pn'] = page     
        return data

class PrinterDetailView(LoginRequiredMixin,generic.DetailView):
    model = Printers

class PrinterCreate(LoginRequiredMixin, BSModalCreateView):
    template_name = 'cartrige/printers_form.html'
    form_class = PrinterModelForm
    success_url = reverse_lazy('printers-list')

class PrinterUpdate(LoginRequiredMixin, BSModalUpdateView):
    model = Printers
    template_name = 'cartrige/printers_form.html'
    form_class = PrinterModelForm

    def get_success_url(self) -> str:
        pn=self.request.GET['page']
        return (reverse_lazy('printers-list')) + '?page='+ pn

class PrinterDelete(LoginRequiredMixin, BSModalDeleteView):
    model = Printers
    success_message = 'Удалено'

    def get_success_url(self) -> str:
        return reverse_lazy('printers-list')

''' Вьюшки для справочника подразделений организации'''
#@permission_required('depart.can_mark_returned')
class DepListView(LoginRequiredMixin,generic.ListView):
    model = Depart
    #paginate_by = 10
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data1 = stat()
        data = super().get_context_data(**kwargs)
        data['all_records'] = data1['all_records']
        data['ost_sklad'] = data1['ost_sklad']
        data['num_rec'] = data1['num_rec']
        data['inwork'] = data1['inwork']
        data['inreserve'] = data1['inreserve']
        data['isempty'] = data1['isempty']
        data['isload'] = data1['isload']
        try:
            page=self.request.GET['page']
        except:
            page=1
        data['pn'] = page     
        return data

class DepDetailView(LoginRequiredMixin,generic.DetailView):
    model = Depart

class DepCreate(LoginRequiredMixin, BSModalCreateView):
    template_name = 'cartrige/dep_form.html'
    form_class = DepartModelForm
    success_url = reverse_lazy('departs-list')

class DepUpdate(LoginRequiredMixin, BSModalUpdateView):
    model = Depart
    template_name = 'cartrige/dep_form.html'
    form_class = DepartModelForm
    success_url = reverse_lazy('departs-list')

class DepDelete(LoginRequiredMixin, BSModalDeleteView):
    model = Depart
    success_url = reverse_lazy('departs-list')
    success_message = 'Удалено'


''' Вьюшки для справочника принтеров организации'''
#@permission_required('allprinters.can_mark_returned')
class AllPrintersListView(LoginRequiredMixin,generic.ListView):
    model = AllPrinters
    #paginate_by = 10
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data1 = stat()
        data = super().get_context_data(**kwargs)
        data['all_records'] = data1['all_records']
        data['ost_sklad'] = data1['ost_sklad']
        data['num_rec'] = data1['num_rec']
        data['inwork'] = data1['inwork']
        data['inreserve'] = data1['inreserve']
        data['isempty'] = data1['isempty']
        data['isload'] = data1['isload']
        try:
            page=self.request.GET['page']
        except:
            page=1
        data['pn'] = page     
        return data

class AllPrintersDetailView(LoginRequiredMixin,generic.DetailView):
    model = AllPrinters

class AllPrintersCreate(LoginRequiredMixin, BSModalCreateView):
    template_name = 'cartrige/allprinters_form.html'
    form_class = AllPrintersModelForm
    success_url = reverse_lazy('allprinters-list')

class AllPrintersUpdate(LoginRequiredMixin, BSModalUpdateView):
    model = AllPrinters
    template_name = 'cartrige/allprinters_form.html'
    form_class = AllPrintersModelForm
    success_url = reverse_lazy('allprinters-list')

class AllPrintersDelete(LoginRequiredMixin, BSModalDeleteView):
    model = AllPrinters
    success_url = reverse_lazy('allprinters-list')
    success_message = 'Удалено'
###########################################################################################

''' Вьюшки для справочника картриджей на складе (новых)'''
#@permission_required('sklad.can_mark_returned')
class SkladListView(generic.ListView):
    model = Sklad
    paginate_by = 20
    
    def get_queryset(self):
        qs = super().get_queryset()
        try:
            cb0 = self.request.COOKIES['cb0']
        except:
            cb0='off'
        if cb0 =='on':
            qs = qs.filter(cart_count__gt=0)
        return qs

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data1 = stat()
        data = super().get_context_data(**kwargs)
        data['all_records'] = data1['all_records']
        data['ost_sklad'] = data1['ost_sklad']
        data['num_rec'] = data1['num_rec']
        data['inwork'] = data1['inwork']
        data['inreserve'] = data1['inreserve']
        data['isempty'] = data1['isempty']
        data['isload'] = data1['isload']
        return data

class SkladCreate(LoginRequiredMixin, BSModalCreateView):
    template_name = 'cartrige/sklad_form.html'
    form_class = SkladModelForm
    success_url = reverse_lazy('sklad-list')

class SkladUpdate(LoginRequiredMixin, BSModalUpdateView):
    model = Sklad
    template_name = 'cartrige/sklad_form.html'
    form_class = SkladModelForm
    success_url = reverse_lazy('sklad-list')

class SkladDelete(LoginRequiredMixin, BSModalDeleteView):
    model = Sklad
    success_url = reverse_lazy('sklad-list')
    success_message = 'Удалено'



''' Вьюшки для справочника метагрупп'''
#@permission_required('metacart.can_mark_returned')
class MetaCartListView(generic.ListView):
    model = MetaCart
    template_name = 'cartrige/meta_list.html'
    paginate_by = 8
    paginate_orphans = 2
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data1 = stat()
        data = super().get_context_data(**kwargs)
        data['all_records'] = data1['all_records']
        data['ost_sklad'] = data1['ost_sklad']
        data['num_rec'] = data1['num_rec']
        data['inwork'] = data1['inwork']
        data['inreserve'] = data1['inreserve']
        data['isempty'] = data1['isempty']
        data['isload'] = data1['isload']
        return data

class MetaCartCreate(LoginRequiredMixin, BSModalCreateView):
    template_name = 'cartrige/meta_form.html'
    form_class = MetaCartModelForm
    success_url = reverse_lazy('meta-list')

class MetaCartUpdate(LoginRequiredMixin, BSModalUpdateView):
    model = MetaCart
    template_name = 'cartrige/meta_form.html'
    form_class = MetaCartModelForm
    success_url = reverse_lazy('meta-list')

class MetaCartDelete(LoginRequiredMixin, BSModalDeleteView):
    model = MetaCart
    success_url = reverse_lazy('meta-list')
    success_message = ''
    
    def get_success_url(self) -> str:
        try:
            pn=self.request.GET['page']
        except:
            pn=1
        return (reverse_lazy('meta-list')) + '?page='+ str(pn)

    def delete(self,request, *args, **kwargs):
        try:
            rend = super(MetaCartDelete, self).delete(request, *args, **kwargs)
            if rend:
                messages.success(request,"Удалено!")
            return rend
        except models.ProtectedError as e:
            success_message = ""
            messages.success(request,"К этой метагруппе привязаны модели картриджей! Перед удалением их необходимо отвязать")
            return HttpResponseRedirect(reverse('meta-list'))


def MoveCart(request,pk):     # передача со склада ######################################################
    skl = get_object_or_404(Sklad, pk=pk)
    form = MoveModelForm()

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':
        
        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = MoveModelForm(request.POST)
        # Проверка валидности данных формы:
        if form.is_valid():
            tmp=form.cleaned_data['id_dep']
            u=request.user.username
            nm=request.POST.get('nmax')
            dep=request.POST.get('id_dep')
            t=request._post['csrfmiddlewaretoken'][0:30]
            if tmp.adm == True:
                st=1
            else:
                st=2

            try:
                k = Records.objects.create(id_cart = form.cleaned_data['cartriges'], id_dep = form.cleaned_data['id_dep'], status = st, charge_num = 0, inventar= form.cleaned_data['nmax'])
                Logging(t,u,2,k.id,"Ввод в эксплуатацию со склада Уч.N {0} и передано '{1}'".format(nm,Depart.objects.get(pk=dep)))
            except:
                pass
            skl.cart_count= form.cleaned_data['cart_count']
            skl.save()
            return HttpResponseRedirect(reverse('sklad-list'))
    else:
        form = MoveModelForm()
        form.initial ={'nmax': NMax(),'cartriges':skl.cartriges, 'cart_count': skl.cart_count - 1}
        return render(request,'cartrige/sklad_move.html', {'form': form})
    

from django.views.generic.edit import FormMixin

''' Вьюшки для списка учтенных картриджей '''
#@permission_required('printers.can_mark_returned')
class RecordListView(FormMixin, generic.ListView):
    model = Records
    paginate_by = 20
    form_class = RecordsStatusForm

        
    def get_queryset(self):
        qs = super().get_queryset()
        
        try:
            dept = self.request.COOKIES['dept']
        except:
            dept=''

        try:
            stat = self.request.COOKIES['stat']
        except:
            stat = ''

        try:
            ord = self.request.COOKIES['ord']
        except:
            ord = ''

        try:
            isknum = self.request.GET['isknum']
        except:
            isknum=''

        if isknum != '':
            qs = qs.filter(inventar=int(isknum))
        else:
            if dept != '':
                qs = qs.filter(id_dep = dept)
            if stat != '':
                qs = qs.filter(status = stat)
            if ord != '':
                if ord == '1':
                    qs = qs.order_by('inventar')
                elif ord == '-1':
                    qs = qs.order_by('-inventar')
                elif ord == '2':
                    qs = qs.order_by('id_cart')
                elif ord == '-2':
                    qs = qs.order_by('-id_cart')
                elif ord == '3':
                    qs = qs.order_by('id_dep')
                elif ord == '-3':
                    qs = qs.order_by('-id_dep')
                elif ord == '4':
                    qs = qs.order_by('status')
                elif ord == '-4':
                    qs = qs.order_by('-status')
                elif ord == '5':
                    qs = qs.order_by('charge_num')
                elif ord == '-5':
                    qs = qs.order_by('-charge_num')
                elif ord == '6':
                    qs = qs.order_by('date_in')
                elif ord == '-6':
                    qs = qs.order_by('-date_in')
                elif ord == '7':
                    qs = qs.order_by('id_cart__metacart')
                elif ord == '-7':
                    qs = qs.order_by('-id_cart__metacart')
                
        return qs

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        data1 = stat()
        data = super().get_context_data(**kwargs)
        data['all_records'] = data1['all_records']
        data['ost_sklad'] = data1['ost_sklad']
        data['num_rec'] = data1['num_rec']
        data['inwork'] = data1['inwork']
        data['inreserve'] = data1['inreserve']
        data['isempty'] = data1['isempty']
        data['isload'] = data1['isload'] 
        try:
            page=self.request.GET['page']
        except:
            page=1
        data['pn'] = page     
        return data

def myRecordCreate(request):
    form = RecordsModelForm()
    if request.method =='POST':
        inv=request.POST.get('nmax')
        dep=request.POST.get('id_dep')
        cart=request.POST.get('id_cart')
        st=request.POST.get('status')
        cn=request.POST.get('charge_num')
        cmt=request.POST.get('comment')
        t=createToken()
        u=request.user.username

        try:
            k=Records.objects.create(id_cart = Cartriges.objects.get(pk=int(cart)), id_dep = Depart.objects.get(pk=int(dep)), status = st, charge_num = cn, inventar= inv, comment= cmt)
            Logging(t,u,1,k.id,"Регистрация N " + inv)
        except:
            pass
        return HttpResponseRedirect(reverse('records-list'))
    form.initial={'nmax':NMax(),'status':2}
    return render(request,'cartrige/record_form.html', {'form': form})    


class RecordUpdate(LoginRequiredMixin,PermissionRequiredMixin, BSModalUpdateView):
    model = Records
    template_name = 'cartrige/record_form.html'
    form_class = RecordsModelForm
    login_url = 'login'
    permission_required = ('cartrige.can_mark_returned', 'cartrige.can_edit')
    oldrec = {}
    newrec = {}
    
    
    def get_success_url(self) -> str:
        pn=self.request.GET['page']
        return (reverse_lazy('records-list')) + '?page='+ pn
    
    def form_valid(self, form) -> HttpResponse:
        #instance = form.save(commit=False)
        self.object = self.get_object()
        self.mes = ""
        u=self.request.user.username
        pk=self.kwargs['pk']
        self.oldrec=Records.objects.get(pk=pk)
        self.newrec=self.request.POST
        self.idcart1 = self.oldrec.id_cart_id
        self.idcart2 = int(self.newrec.get('id_cart'))
        self.iddep1 = self.oldrec.id_dep_id
        self.iddep2 = int(self.newrec.get('id_dep'))
        self.charge1 = self.oldrec.charge_num
        self.charge2 = int(self.newrec.get('charge_num'))
        self.status1 = self.oldrec.status
        self.status2 = int(self.newrec.get('status'))
        self.comment1 = self.oldrec.comment
        if self.comment1==None:
            self.comment1=''
        self.comment2 = self.newrec.get('comment')
        if self.idcart1 != self.idcart2:
            self.mes = "Замена модели: '{0}' на '{1}'; ".format(Cartriges.objects.get(pk=self.idcart1),Cartriges.objects.get(pk=self.idcart2))
        if self.iddep1 != self.iddep2:
            self.mes += "Замена подразделения: '{0}' на '{1}'; ".format(Depart.objects.get(pk=self.iddep1),Depart.objects.get(pk=self.iddep2))
        if self.charge1 != self.charge2:
            self.mes += "Изменено количество заправок: {0} на {1}; ".format(self.charge1,self.charge2)
        if self.status1 != self.status2:
            self.mes += "Изменен статус: {0} на {1}; ".format(self.status1, self.status2)
        if self.comment1 != self.comment2:
            self.mes += "Обновлен комментарий: '{0}' на '{1}'".format(self.comment1, self.comment2)
        if self.mes != "":
            self.t=self.request._post['csrfmiddlewaretoken'][0:31]
        try:
            Logging(self.t,u,3,pk,"Редактирование N {0}: {1}".format(self.oldrec.inventar,self.mes))
        except:
            pass
        if self.status1 != self.status2 and self.status2==2:
            try:
                Logging(self.t[0:30]+"a",u,5,pk,"Выдача заправленного - N {0}".format(self.oldrec.inventar,))
            except:
                pass
        #instance.save()
        return super().form_valid(form) #HttpResponseRedirect(reverse('records-list')) #
    
    
class RecordDelete(LoginRequiredMixin,PermissionRequiredMixin, BSModalDeleteView):
    model = Records
    success_message = 'Удалено'
    permission_required = ('cartrige.can_mark_returned', 'cartrige.can_edit')
    
    def get_success_url(self) -> str:
        pn=self.request.GET['page']
        u=self.request.user.username
        pk=self.kwargs['pk']
        rec = Records.objects.get(pk=pk)
        t=self.request._post['csrfmiddlewaretoken'][0:31]
        Logging(t,u,8,pk,"Удалено N " + str(rec.inventar) + ", модель: " + str(rec.id_cart))
        return (reverse_lazy('records-list')) + '?page='+ pn

def RecordChange(request):  # замена сданного на заправленный
    data1=""
    reserv=""
    skl=""
    isknum = request.GET.get("isknum",default="")
    if isknum != "":
        #if Records.objects.get(inventar=int(isknum),status=2):
        try:
            data1=Records.objects.get(inventar=int(isknum),status=2)
        except:
            isknum=""

        if data1 != "":
            #for dd in data:
            #    mt = dd.id_cart.metacart
            mt = data1.id_cart.metacart
            reserv = Records.objects.filter(status__in = {1,5}, id_cart__metacart = mt.id).order_by('status','id_cart')
            skl = Sklad.objects.filter(cartriges__metacart = mt.id, cart_count__gt=0)
    
    data = stat()
    all_records = data['all_records']
    ost_sklad = data['ost_sklad']
    num_rec = data['num_rec']
    inwork = data['inwork']
    inreserve = data['inreserve']
    isempty = data['isempty']
    isload = data['isload']
        
    id = request.GET.get("in_cart", default="")
    if id !="":
        sel_cand= request.GET.get("sel_cand", default="")
        u=request.user.username
        b4=Records.objects.get(inventar=id) 
        out1=Records.objects.get(pk=sel_cand)
        b4.status = 3
        out1.status = 2
        b4.id_dep, out1.id_dep = out1.id_dep, b4.id_dep
        
        b4.save(update_fields=['status','id_dep'])
        out1.save(update_fields=['status','id_dep'])
        t=createToken()
        Logging(t,u,4,b4.id,"Прием пустого - N {0} от '{1}'".format(b4.inventar, out1.id_dep))
        t=createToken()
        Logging(t,u,5,out1.id,"Выдача заправленного - N {0} > '{1}'".format(out1.inventar, out1.id_dep))
        return HttpResponseRedirect(reverse('records-list'))
    else:
        return render(
            request,
            'cartrige/record_change.html',
            context={'all_records' : all_records, 
            'ost_sklad' : ost_sklad, 
            'num_rec' : num_rec, 
            'data1' : data1,
            'isknum' : isknum, 
            'reserv' : reserv, 
            'skl' : skl, 
            'inwork' : inwork, 
            'inreserve' : inreserve, 
            'isempty' : isempty, 
            'isload' : isload},
        )
    

def MoveCart2Use(request,pk):     # передача со склада в обмен сданного ################################
    skl = get_object_or_404(Sklad, pk=pk)
    form = MoveModelForm()

    if request.method == 'POST':
        u=request.user.username
        nm=request.POST.get('nmax')
        dep=request.POST.get('id_dep')
        cart=request.POST.get('cartriges')
        isk=request.POST.get('isk')
        t=request._post['csrfmiddlewaretoken'][0:30]
        try:
            k=Records.objects.create(id_cart = Cartriges.objects.get(pk=int(cart)), id_dep = Depart.objects.get(pk=int(dep)), status = 2, charge_num = 0, inventar= int(nm))
            skl.cart_count -= 1 
            skl.save()
            Logging(t,u,2,k.id,"Ввод в эксплуатацию со склада N {0} и передано '{1}'".format(nm,Depart.objects.get(pk=dep)))

            b4=Records.objects.get(inventar=int(isk))
            b4.status = 3
            b4.id_dep = Depart.objects.get(adm=True)
            b4.save(update_fields=['status','id_dep'])
            t=createToken()
            Logging(t,u,4,b4.id,"Прием пустого - N {0} от '{1}'".format(isk, Depart.objects.get(pk=dep)))
        except:
            pass
        
        return HttpResponseRedirect(reverse('records-list'))
    
    dep = request.GET.get('dep')
    isk = request.GET.get("isk")
    form.initial ={'nmax': NMax(),'cartriges':skl.cartriges, 'cart_count': skl.cart_count, 'id_dep': dep, 'isk': isk}
    return render(request,'cartrige/sklad_move.html', {'form': form})

def PrintView(request):     # формирование печатной формы передаваемых на заправку
    cc=()
    partner=''
    cartriges=''
    reccount=0
    cc = tuple(request.GET.getlist('cc'))
    ca = request.GET.get('ca',default="")
    if cc!=():
        cartriges = Records.objects.filter(id__in=cc).order_by('id_cart_id__name_cart')
        reccount = Records.objects.filter(id__in=cc).count()
    if ca!='':
        partner = ContrAgent.objects.get(id=ca)
    dt = datetime.datetime.today().strftime("%d.%m.%Y")
    nach = Depart.objects.get(adm=True)
    organ = ContrAgent.objects.get(adm=True)
    return render(
        request,
        'cartrige/print.html',
        context={'cartriges':cartriges,'partner':partner, 'reccount':reccount, 'dt':dt, 'nach':nach, 'organ':organ},
        )

def CartSend(request):      # Процедура передачи на заправку
    empties = ""
    cc=""
    empties = Records.objects.filter(status=3).order_by('id_cart')
    contragent = ContrAgent.objects.filter(adm=False)

    data = stat()
    all_records = data['all_records']
    ost_sklad = data['ost_sklad']
    num_rec = data['num_rec']
    inwork = data['inwork']
    inreserve = data['inreserve']
    isempty = data['isempty']
    isload = data['isload']

    if request.method == 'POST':
        cc = tuple(request.POST.getlist('sel_cand'))
        ca = request.POST.get('id_contragent',default="")
        ra = request.META['REMOTE_ADDR']
        t=request._post['csrfmiddlewaretoken'][0:28]
        if ca!='':
            partner = ContrAgent.objects.get(id=ca)
        u=request.user.username
        if cc!=():
            
            for i in cc:
                cartrige = Records.objects.get(pk=int(i))
                cartrige.status=4
                cartrige.c_agent = ContrAgent.objects.get(pk=int(ca))
                cartrige.date_out = datetime.datetime.today()
                cartrige.save()
                Logging(t+str(i),u,6,int(i),"Передано на заправку - N {0} - '{1}'".format(cartrige.inventar,partner.name_agent)) # + ' (' + ra +")")
        return HttpResponseRedirect(reverse('records-send'))
        #else:
        #    return HttpResponseRedirect(reverse('records-send'))

    return render(
        request,
        'cartrige/zapravka.html',
        context={'all_records' : all_records, 
        'ost_sklad' : ost_sklad, 
        'num_rec' : num_rec, 
        'empties' : empties, 
        'contragent' : contragent, 
        'inwork' : inwork, 
        'inreserve' : inreserve, 
        'isempty' : isempty, 
        'isload' : isload},
        )

def CartReceive(request):      # Процедура приема с заправки
    empties = ""
    cc=""
    ca = request.GET.get('id_contragent',default="")
    if ca!='':
        empties = Records.objects.filter(status=4,c_agent=ContrAgent.objects.get(pk=int(ca))).order_by('id_cart')
    else:
        empties = Records.objects.filter(status=4).order_by('id_cart')
    contragent = ContrAgent.objects.filter(adm=False)

    data = stat()
    all_records = data['all_records']
    ost_sklad = data['ost_sklad']
    num_rec = data['num_rec']
    inwork = data['inwork']
    inreserve = data['inreserve']
    isempty = data['isempty']
    isload = data['isload']

    if request.method == 'POST':
        cc = tuple(request.POST.getlist('sel_cand'))
        u=request.user.username
        t=request._post['csrfmiddlewaretoken'][0:28]
        if cc!=():
            
            for i in cc:
                cartrige = Records.objects.get(pk=int(i))
                cartrige.status=5
                cartrige.charge_num += 1
                cartrige.date_out = None
                cartrige.c_agent = None
                cartrige.save()
                Logging(t+str(i),u,7,int(i),"Получено с заправки- N {0}".format(cartrige.inventar,))
               
        return HttpResponseRedirect(reverse('records-receive'))

    return render(
        request,
        'cartrige/receive.html',
        context={'all_records' : all_records, 
        'ost_sklad' : ost_sklad, 
        'num_rec' : num_rec, 
        'empties' : empties, 
        'contragent' : contragent, 
        'ca' : ca, 
        'inwork' : inwork, 
        'inreserve' : inreserve, 
        'isempty' : isempty, 
        'isload' : isload},
        )

def LogStata(request):
    data={}
    data_sum={}
    inf = {}
    static = request.GET.get('static',default="")
    isknum = request.GET.get('isknum',default="")
    if static == "":
        try:
            static=request.COOKIES['static']
        except:
            static=""
            
    query3 = '''DROP TABLE IF EXISTS `cartrige_tmp`;
CREATE TABLE `cartrige_tmp` (
  `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `god` int NOT NULL DEFAULT '0',
  `meta` varchar(40) DEFAULT NULL,
  `oper` varchar(25) DEFAULT NULL,
  `actid` int NOT NULL DEFAULT '0',
  `m1` int NOT NULL DEFAULT '0',
  `m2` int NOT NULL DEFAULT '0',
  `m3` int NOT NULL DEFAULT '0',
  `m4` int NOT NULL DEFAULT '0',
  `m5` int NOT NULL DEFAULT '0',
  `m6` int NOT NULL DEFAULT '0',
  `m7` int NOT NULL DEFAULT '0',
  `m8` int NOT NULL DEFAULT '0',
  `m9` int NOT NULL DEFAULT '0',
  `m10` int NOT NULL DEFAULT '0',
  `m11` int NOT NULL DEFAULT '0',
  `m12` int NOT NULL DEFAULT '0',
  `msum` int NOT NULL DEFAULT '0',
  `ord` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


COMMIT;

'''

    query4 = '''INSERT INTO `cartrige_tmp`(god, meta, oper, actid, m{0}, ord) 
SELECT YEAR(date_event), metatitle, operation_name, action_id, count(obj),1 
FROM (((`cartrige_logs`INNER JOIN `cartrige_operation` ON action_id=kod)
INNER JOIN `cartrige_records` ON obj=`cartrige_records`.id)
INNER JOIN `cartrige_cartriges` ON id_cart_id=`cartrige_cartriges`.id)
INNER JOIN `cartrige_metacart` ON metacart_id=`cartrige_metacart`.id
WHERE MONTH(date_event)={1} and action_id in (1,2,5,6,7)
GROUP BY YEAR(date_event), metatitle, operation_name, action_id;'''

    query6 = '''INSERT INTO `cartrige_tmp`(god, meta, oper, actid, m{0}, ord) 
SELECT YEAR(date_event), name_cart, operation_name, action_id, count(obj),1 
FROM ((`cartrige_logs`INNER JOIN `cartrige_operation` ON action_id=kod)
INNER JOIN `cartrige_records` ON obj=`cartrige_records`.id)
INNER JOIN `cartrige_cartriges` ON id_cart_id=`cartrige_cartriges`.id
WHERE MONTH(date_event)={1} and action_id in (1,2,5,6,7)
GROUP BY YEAR(date_event), name_cart, operation_name, action_id;'''

    query5 = '''INSERT INTO `cartrige_tmp`(god, meta, oper, actid, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, ord) 
SELECT god, meta, oper, actid, sum(m1), sum(m2), sum(m3), sum(m4), sum(m5), sum(m6), sum(m7), sum(m8), sum(m9), sum(m10), sum(m11), sum(m12), 2
FROM `cartrige_tmp`
WHERE ord=1
GROUP BY god,meta,oper,actid;

INSERT INTO `cartrige_tmp`(god, meta, oper, actid, m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,msum, ord) 
SELECT god, meta, oper, actid, m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,sum(m1+m2+m3+m4+m5+m6+m7+m8+m9+m10+m11+m12), 3
FROM `cartrige_tmp`
WHERE ord=2
GROUP BY god,meta,oper,actid, m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12
ORDER BY god,meta,actid;

INSERT INTO `cartrige_tmp`(god, meta, oper, actid, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, msum, ord) 
SELECT god, 'Всего', oper, actid, sum(m1), sum(m2), sum(m3), sum(m4), sum(m5), sum(m6), sum(m7), sum(m8), sum(m9), sum(m10), sum(m11), sum(m12), sum(msum),4
FROM `cartrige_tmp`
WHERE ord=3
GROUP BY god,oper,actid
ORDER BY god,actid;
'''


    infdata = stat()
    all_records = infdata['all_records']
    ost_sklad = infdata['ost_sklad']
    num_rec = infdata['num_rec']
    inwork = infdata['inwork']
    inreserve = infdata['inreserve']
    isempty = infdata['isempty']
    isload = infdata['isload']

    #data_all = Logs.objects.raw(query1)
    #data = Logs.objects.raw(query1)
    if static=='1':
        with connection.cursor() as cursor:
            cursor.execute(query3)
            for i in range(12):
                cursor.execute(query4.format(str(i+1),str(i+1)))
            cursor.execute(query5)
        data = Tmp.objects.filter(ord__in=(3,4))
        data_sum = Tmp.objects.filter(ord=4)
    elif static=='2':
        if isknum!='':
            try:
                ipk= Records.objects.get(inventar=int(isknum))
            except:
                ipk=""
            if ipk != "":
                pk = ipk.id
                inf = Logs.objects.filter(obj = pk).order_by('date_event')
    elif static=='3':
        with connection.cursor() as cursor:
            cursor.execute(query3)
            for i in range(12):
                cursor.execute(query6.format(str(i+1),str(i+1)))
            cursor.execute(query5)
        data = Tmp.objects.filter(ord__in=(3,4))
        data_sum = Tmp.objects.filter(ord=4)


    return render(
        request,
        'cartrige/stata.html',
        context={'data' : data,
        'data_sum' : data_sum,
        'all_records' : all_records, 
        'ost_sklad' : ost_sklad, 
        'num_rec' : num_rec,
        'inwork' : inwork, 
        'inreserve' : inreserve, 
        'isempty' : isempty, 
        'isload' : isload,
        'inf' : inf,
        'isknum' : isknum}, #'data_all' : data_all, 
    )

