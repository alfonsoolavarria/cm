from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .views import (Maracay, Account, Conditions,Login,Logout,Profile, Help, We,
    Places, Payment, Delivery, ControlAdmin, AllProducts,FrigorificoProducts,
    EnlatadosProducts,ViveresProducts, CartShopping, CartOrder, ConfimationOrder,HelpForm,
    CartOrderEntrega,Restore,Forgot,ForgotMail,AllProductsAdmin,ViveresProductsAdmin,
    FrigorificoProductsAdmin,EnlatadosProductsAdmin,Detail)
from django.conf import settings
from django.conf.urls import url
from maracay import verificacion_compras,agrega_costo

urlpatterns = [
    url(r'^$', Maracay.as_view(), name='maracay'),
    url(r'^account/$', Account.as_view(), name='account'),
    url(r'^conditions/$', Conditions, name='Conditions'),
    url(r'^login/$', csrf_exempt(Login.as_view()), name='login'),
    url(r'^logout/$', csrf_exempt(Logout.as_view()), name='logout'),
    url(r'^restore/$', Restore, name='restorepagina'),
    url(r'^forgot/password/$', Forgot, name='restoreenvio'),
    url(r'^forgot/password/mail/$', ForgotMail, name='restoredesdeemail'),
    url(r'^profile/$', csrf_exempt(Profile.as_view()), name='profile'),
    url(r'^help/$', Help, name='help'),
    url(r'^help/form/$', csrf_exempt(HelpForm), name='helpform'),
    url(r'^we/$', We, name='we'),
    url(r'^places/$', Places, name='places'),
    url(r'^payment/$', Payment, name='payment'),
    url(r'^delivery/$', Delivery, name='delivery'),
    #administrador
    url(r'^criollitos/market/admin/$', ControlAdmin.as_view(), name='admin'),
    url(r'^criollitos/market/admin/all/$', AllProductsAdmin, name='adminall'),
    url(r'^criollitos/market/admin/viveres/$', ViveresProductsAdmin, name='adminviveres'),
    url(r'^criollitos/market/admin/frigorifico/$', FrigorificoProductsAdmin, name='adminfrigorifico'),
    url(r'^criollitos/market/admin/enlatados/$', EnlatadosProductsAdmin, name='adminenlatados'),
    #filtros
    url(r'^all/$', AllProducts, name='all'),
    url(r'^viveres/$', ViveresProducts, name='viveres'),
    url(r'^frigorifico/$', FrigorificoProducts, name='frigorifico'),
    url(r'^enlatados/$', EnlatadosProducts, name='enlatados'),
    #carrito de compras
    url(r'^cart/shopping/$', csrf_exempt(CartShopping), name='cartshopping'),
    #caja de compras
    url(r'^cart/order/$', csrf_exempt(CartOrder), name='cartsorder'),
    #compra finalizada
    url(r'^orden/entrega/$', csrf_exempt(CartOrderEntrega), name='cartsorderentrega'),
    #confirmacion de pedido
    url(r'^confirmacion/$', csrf_exempt(ConfimationOrder), name='confirmacioncompra'),
    #detales de la compra
    url(r'^detalles/$', csrf_exempt(Detail), name='detail'),


]
#proceso trabajoRecursivo
#verificacion_compras()

#proces de agregar costo de envio
agrega_costo()
