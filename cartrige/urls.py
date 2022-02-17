from django.urls import path, include
from . import views
#from . import forms
from django.conf.urls import url
#from django.contrib.auth import authenticate, login
#from .forms import MyAuthForm
from django.contrib.auth import views as auth_views
#from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #path('login/', csrf_exempt(views.CustomLoginView.as_view()), name='login'),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
]

urlpatterns += [
    url(r'^cartriges/$', views.CartrigeListView.as_view(), name='cartriges-list'),
    #url(r'^cartriges/create/$', views.CartrigeCreate.as_view(), name='cartriges-create'),
    url(r'^cartriges/create/$', views.CartCreateView.as_view(), name='cartriges-create'),
    url(r'^cartriges/(?P<pk>\d+)/update/$', views.CartrigeUpdate.as_view(), name='cartriges-update'),
    url(r'^cartriges/(?P<pk>\d+)/delete/$', views.CartrigeDelete.as_view(), name='cartriges-delete'),
]

urlpatterns += [
    url(r'^groups/$', views.MetaCartListView.as_view(), name='meta-list'),
    url(r'^groups/create/$', views.MetaCartCreate.as_view(), name='meta-create'),
    url(r'^groups/(?P<pk>\d+)/update/$', views.MetaCartUpdate.as_view(), name='meta-update'),
    url(r'^groups/(?P<pk>\d+)/delete/$', views.MetaCartDelete.as_view(), name='meta-delete'),
]

urlpatterns += [
    url(r'^printers/$', views.PrinterListView.as_view(), name='printers-list'),
#    url(r'^printers/(?P<pk>\d+)$', views.PrinterDetailView.as_view(), name='printers-detail'),
    url(r'^printers/create/$', views.PrinterCreate.as_view(), name='printers-create'),
    url(r'^printers/(?P<pk>\d+)/update/$', views.PrinterUpdate.as_view(), name='printers-update'),
    url(r'^printers/(?P<pk>\d+)/delete/$', views.PrinterDelete.as_view(), name='printers-delete'),
]

urlpatterns += [
    url(r'^departments/$', views.DepListView.as_view(), name='departs-list'),
    url(r'^departments/create/$', views.DepCreate.as_view(), name='departs-create'),
    url(r'^departments/(?P<pk>\d+)/update/$', views.DepUpdate.as_view(), name='departs-update'),
    url(r'^departments/(?P<pk>\d+)/delete/$', views.DepDelete.as_view(), name='departs-delete'),
]

urlpatterns += [
    url(r'^allprinters/$', views.AllPrintersListView.as_view(), name='allprinters-list'),
    url(r'^allprinters/create/$', views.AllPrintersCreate.as_view(), name='allprinters-create'),
    url(r'^allprinters/(?P<pk>\d+)/update/$', views.AllPrintersUpdate.as_view(), name='allprinters-update'),
    url(r'^allprinters/(?P<pk>\d+)/delete/$', views.AllPrintersDelete.as_view(), name='allprinters-delete'),
]

urlpatterns += [
    url(r'^sklad/$', views.SkladListView.as_view(), name='sklad-list'),
    url(r'^sklad/create/$', views.SkladCreate.as_view(), name='sklad-create'),
    url(r'^sklad/(?P<pk>\d+)/update/$', views.SkladUpdate.as_view(), name='sklad-update'),
    url(r'^sklad/(?P<pk>\d+)/delete/$', views.SkladDelete.as_view(), name='sklad-delete'),
    url(r'^sklad/move/(?P<pk>\d+)/$', views.MoveCart, name='move-cart'),
]

urlpatterns += [
    url(r'^records/$', views.RecordListView.as_view(), name='records-list'),
    url(r'^records/create/$', views.myRecordCreate, name='record-create'),
    url(r'^records/(?P<pk>\d+)/update/$', views.RecordUpdate.as_view(), name='record-update'),
    url(r'^records/(?P<pk>\d+)/delete/$', views.RecordDelete.as_view(), name='record-delete'),
    url(r'^records/change/$', views.RecordChange, name='record-change'),
    url(r'^records/move/(?P<pk>\d+)/$', views.MoveCart2Use, name='move-cart2'),
    url(r'^records/send/$', views.CartSend, name='records-send'),
    url(r'^records/send/print/$', views.PrintView, name='records-send-print'),
    url(r'^records/receive/$', views.CartReceive, name='records-receive'),
]

urlpatterns += [
    url(r'^logs/$', views.LogStata, name='log-stata'),
]
    #url(r'^records/change/plus/$', views.RecordPlus.as_view(), name='change-plus'),
    #url(r'^records/create/$', views.RecordCreate.as_view(), name='record-create'),