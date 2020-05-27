from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from maracay.backEnd import backStart, profileBackend, filterProducts, adminSite
from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from threading import Thread
from maracay.models import Tools, Profile as ProfileDB, PurchaseConfirmation, TokenPassword, PagosImagenes
from maracay import get_client_ip, config
import json,random, string, datetime
from django.contrib import admin
import os
from maracay.sendinblue import sendinblue_send
# Create your views here.
#Main Class
class Maracay(TemplateView):
    template_name = 'market/index.html'
    #index
    def get(self, request, *args, **kwargs):
        _allproducts = backStart(request)

        _allproducts.get()
        if 'pagination' not in request.GET:
            data = _allproducts.response_data
            data['code'] = _allproducts.code

            contact_list = data['cantTotal']
            paginator = Paginator(contact_list, 10) # Show 25 contacts per page
            page = request.GET.get('page')
            contacts = paginator.get_page(page)
            direction = '/static/images/upload/imagesp/'
            return render(request, 'market/index.html',{'direction':direction,'contacts':contacts,'data':json.dumps(data['data'])})
        '''else:
            print ("22222")
            data = _allproducts.response_data
            data['code'] = _allproducts.code

            contact_list = data['cantTotal']
            paginator = Paginator(contact_list, 10) # Show 25 contacts per page
            page = request.GET.get('page')
            contacts = paginator.get_page(page)
            dataAll = {'contacts':contacts}
            return HttpResponse(json.dumps(dataAll, cls=DjangoJSONEncoder), content_type='application/json')'''



class Account(View):
    def get(self, request, *args, **kwargs):
        if str(request.user) != 'AnonymousUser':#si esta logeado su data
            _accountData = profileBackend(request)
            _accountData.accountData()
            data = _accountData.response_data
            return render(request, 'market/account.html', {'data':data['data']})
        else: # registro
            return render(request, 'market/register.html', {})


class Login(View):
    def __init__(self):
        self.requireds = ['email', 'password', 'csrfmiddlewaretoken']

    def post(self, request, *args, **kwargs):
        # __ip = get_client_ip(request)
        for key in self.requireds:
            if not key in request.POST.keys():
                return HttpResponse(status=400, content_type='application/json')
        for session in Session.objects.filter(session_key=request.session.session_key):
            if session:
                #No se puede iniciar Sesion usuario ya tiene una sesion activa
                return HttpResponse(json.dumps({'code':400,'message':'Ya tiene una sesiòn activa'}, cls=DjangoJSONEncoder), content_type='application/json')

        # if cache.get('cache_ip__%s'%__ip):
        #     return HttpResponse(json.dumps({'code':400,'message':'Debe esperar 5 minutos'}, cls=DjangoJSONEncoder), content_type='application/json')

        user = authenticate(username=request.POST['email'], password=request.POST['password'])

        if user:
            cache.clear()
            login(request, user)
            return HttpResponse(json.dumps({'code':200}, cls=DjangoJSONEncoder), content_type='application/json')

        else:
            return HttpResponse(json.dumps({'code':400,'message':'Intento fallido'}, cls=DjangoJSONEncoder), content_type='application/json')
        #
        #     __cache_count_error = cache.get('cache_error__%s'%__ip)
        #     __cache_exist = cache.get('cache_ip__%s'%__ip)

            # if __cache_exist:
            #     return HttpResponse(json.dumps({'code':400,'message':'Debe esperar 5 minutos'}, cls=DjangoJSONEncoder), content_type='application/json')
            # else:
            #     if __cache_count_error:
            #         if __cache_count_error == 1:
            #             cache.set('cache_error__%s'%__ip,1+1,60)
            #             return HttpResponse(json.dumps({'code':400,'message':'Segundo intento fallido'}, cls=DjangoJSONEncoder), content_type='application/json')
            #         elif __cache_count_error == 2:
            #             cache.set('cache_ip__%s'%__ip,__ip,300)
            #             return HttpResponse(json.dumps({'code':400,'message':'Tercer intento fallido/Debe esperar 5 minutos'}, cls=DjangoJSONEncoder), content_type='application/json')
            #     else:
            #         cache.set('cache_error__%s'%__ip,1,60)
            #         return HttpResponse(json.dumps({'code':400,'message':'Primer intento fallido'}, cls=DjangoJSONEncoder), content_type='application/json')

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)

        _allproducts = backStart(request)
        _allproducts.get('all')
        data = _allproducts.response_data
        data['code'] = _allproducts.code
        return render(request, 'market/index.html',{'data':data['data'][0] if data['data'] else {} })


class Profile(View):
    def get(self, request, *args, **kwargs):
        print ("Profile")

    #creacion de usuarios
    def post(self, request, *args, **kwargs):
        _newUser = profileBackend(request)
        _newUser.post()
        data = _newUser.response_data
        data['code'] = _newUser.code
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user:login(request, user)
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

    def put(self, request, *args, **kwargs):
        request.POST=QueryDict(request.read())
        try:
            data = {'code':200}
            if request.POST['flagProfileonly'] == 'false':
                dataUser = User.objects.get(pk=int(request.POST['user']))
                dataUser.first_name=request.POST['name']
                dataUser.last_name=request.POST['lastname']

                dataProfile = ProfileDB.objects.get(user=dataUser.id)
                dataProfile.phone=request.POST['phone']
                dataProfile.rif=request.POST['rif']
                dataUser.save()
                dataProfile.save()
            else:
                dataProfile = ProfileDB.objects.get(user=User.objects.get(pk=int(request.POST['user'])))
                dataProfile.direction=request.POST['direction']
                dataProfile.localphone=request.POST['localphone']
                dataProfile.reference=request.POST['reference']
                dataProfile.save()

            return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        except Exception as e:
            print (e)
            data = {'code':500}
            return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

#Seccion de Administrador
def AllProductsAdminTable(request):
    #poner esto and request.user.is_superuser==True para el admin
    # if str(request.user) != 'AnonymousUser' :#si esta logeado su data
    _allproductstable = adminSite(request)
    _allproductstable.allProductsTable()
    data = _allproductstable.response_data
    print("data",data)
    # data = {"a":"a"}
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
    # else:
    #     return render(request, 'market/adminIndex.html', {})


class ControlAdmin(View):
    def get(self, request, *args, **kwargs):
        #poner esto and request.user.is_superuser==True para el admin
        if str(request.user) != 'AnonymousUser' :#si esta logeado su data
            _allproductsfilter = adminSite(request)
            _allproductsfilter.dataProductUser()

            data = _allproductsfilter.response_data
            data['code'] = _allproductsfilter.code
            contact_list = data['cantTotal']
            paginator = Paginator(contact_list, 10) # Show 25 contacts per page
            page = request.GET.get('page')
            contacts = paginator.get_page(page)
            dataAll = {'contacts':contacts}
            direction = '/static/images/upload/imagesp/'
            return render(request, 'market/adminGestion.html', {'direction':direction,'data':contacts,'flag':'all'})
        else: # registro
            return render(request, 'market/adminIndex.html', {})

#Fin de la Seccion de Administrador

def Conditions(request):
    return render(request, 'market/conditions.html', {})

def Help(request):
    return render(request, 'market/help.html', {})

def We(request):
    return render(request, 'market/we.html', {})

def Places(request):
    return render(request, 'market/places.html', {})

def Payment(request):
    return render(request, 'market/payment.html', {})

def Delivery(request):
    return render(request, 'market/delivery.html', {})


####CARRITO DE COMPRAS#####
def CartShopping(request):
    if str(request.user) != 'AnonymousUser':#si esta logeado su data
        try:
            dataUser = User.objects.get(email=request.user)
            return render(request, 'market/cartshopping.html', {
                'name':dataUser.first_name,
                'apellido':dataUser.last_name,
                'phone':dataUser.user_profile.phone,
                'direction':dataUser.user_profile.direction,
                'rif':dataUser.user_profile.rif,
                'localphone':dataUser.user_profile.localphone,
                'reference':dataUser.user_profile.reference,
                'costoenvio':Tools.objects.get().costoenvio,
                'code':200
            })
        except Exception as e:
            print (e)
            return render(request, 'market/cartshopping.html', {'costoenvio':Tools.objects.get().costoenvio})
    else:
        try:
            return render(request, 'market/cartshopping.html', {'costoenvio':Tools.objects.get().costoenvio})
        except Tools.DoesNotExist:
            data = {'costoenvio':config.COSTO_ENVIO,'create_at':datetime.datetime.now()}
            costo = Tools(**data)
            costo.save()
            return HttpResponseRedirect("/")
        except Exception as e:
            return HttpResponseRedirect("/")


#Section Filters
def AllProducts(request):
    _allproductsfilter = filterProducts(request)
    _allproductsfilter.allProductsFilter()

    data = _allproductsfilter.response_data
    data['code'] = _allproductsfilter.code

    contact_list = data['cantTotal']
    paginator = Paginator(contact_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    dataAll = {'contacts':contacts}
    direction = '/static/images/upload/imagesp/'
    return render(request, 'market/allProducts.html',{'all':1,'direction':direction,'contacts':contacts,'data':json.dumps(data['data'])})

def ViveresProducts(request):
    _viveresproductsfilter = filterProducts(request)
    _viveresproductsfilter.viveresProductsFilter()

    data = _viveresproductsfilter.response_data
    data['code'] = _viveresproductsfilter.code

    contact_list = data['cantTotal']
    paginator = Paginator(contact_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    dataAll = {'contacts':contacts}
    direction = '/static/images/upload/imagesp/'
    return render(request, 'market/viveresProducts.html',{'viveres':1,'direction':direction,'contacts':contacts,'data':json.dumps(data['data'])})

def FrigorificoProducts(request):
    _frigorificoproductsfilter = filterProducts(request)
    _frigorificoproductsfilter.frigorificoProductsFilter()

    data = _frigorificoproductsfilter.response_data
    data['code'] = _frigorificoproductsfilter.code

    contact_list = data['cantTotal']
    paginator = Paginator(contact_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    dataAll = {'contacts':contacts}
    direction = '/static/images/upload/imagesp/'
    return render(request, 'market/frigorificoProducts.html',{'direction':direction,'contacts':contacts,'data':json.dumps(data['data'])})

def EnlatadosProducts(request):
    _enlatadosproductsfilter = filterProducts(request)
    _enlatadosproductsfilter.enlatadosProductsFilter()

    data = _enlatadosproductsfilter.response_data
    data['code'] = _enlatadosproductsfilter.code

    contact_list = data['cantTotal']
    paginator = Paginator(contact_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    dataAll = {'contacts':contacts}
    direction = '/static/images/upload/imagesp/'
    return render(request, 'market/enlatadosProducts.html',{'direction':direction,'contacts':contacts,'data':json.dumps(data['data'])})

def CharcuteriaProducts(request):
    _charcuteriaproductsfilter = filterProducts(request)
    _charcuteriaproductsfilter.charcuteriaProductsFilter()

    data = _charcuteriaproductsfilter.response_data
    data['code'] = _charcuteriaproductsfilter.code

    contact_list = data['cantTotal']
    paginator = Paginator(contact_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    dataAll = {'contacts':contacts}
    direction = '/static/images/upload/imagesp/'
    return render(request, 'market/charcuteriaProducts.html',{'charcuteria':1,'direction':direction,'contacts':contacts,'data':json.dumps(data['data'])})

def CarnesProducts(request):
    _carnesproductsfilter = filterProducts(request)
    _carnesproductsfilter.carnesProductsFilter()

    data = _carnesproductsfilter.response_data
    data['code'] = _carnesproductsfilter.code

    contact_list = data['cantTotal']
    paginator = Paginator(contact_list, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    dataAll = {'contacts':contacts}
    direction = '/static/images/upload/imagesp/'
    return render(request, 'market/carnesProducts.html',{'carne':1,'direction':direction,'contacts':contacts,'data':json.dumps(data['data'])})


#Section Filter Prodcuts Admin
def AllProductsAdmin(request):
    if str(request.user) != 'AnonymousUser':#si esta logeado su data
        _allproductsfilter = adminSite(request)
        _allproductsfilter.dataProductUser()

        data = _allproductsfilter.response_data
        data['code'] = _allproductsfilter.code

        contact_list = data['cantTotal']
        paginator = Paginator(contact_list, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        dataAll = {'contacts':contacts}
        direction = '/static/images/upload/imagesp/'
        return render(request, 'market/adminGestion.html', {'direction':direction,'data':contacts,'flag':'all'})
    else:
        return render(request, 'market/adminIndex.html', {})

def ViveresProductsAdmin(request):
    if str(request.user) != 'AnonymousUser':#si esta logeado su data
        _viveresproductsfilter = adminSite(request)
        _viveresproductsfilter.viveresProductsFilterAdmin()

        data = _viveresproductsfilter.response_data
        data['code'] = _viveresproductsfilter.code

        contact_list = data['cantTotal']
        paginator = Paginator(contact_list, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        dataAll = {'contacts':contacts}
        direction = '/static/images/upload/imagesp/'
        return render(request, 'market/adminGestion.html', {'direction':direction,'data':contacts,'flag':'vive'})
    else:
        return render(request, 'market/adminIndex.html', {})

def FrigorificoProductsAdmin(request):
    if str(request.user) != 'AnonymousUser':#si esta logeado su data
        _frigorificoproductsfilter = adminSite(request)
        _frigorificoproductsfilter.frigorificoProductsFilterAdmin()

        data = _frigorificoproductsfilter.response_data
        data['code'] = _frigorificoproductsfilter.code

        contact_list = data['cantTotal']
        paginator = Paginator(contact_list, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        dataAll = {'contacts':contacts}
        direction = '/static/images/upload/imagesp/'
        return render(request, 'market/adminGestion.html', {'direction':direction,'data':contacts,'flag':'frigo'})
    else:
        return render(request, 'market/adminIndex.html', {})

def EnlatadosProductsAdmin(request):
    if str(request.user) != 'AnonymousUser':#si esta logeado su data
        _enlatadosproductsfilter = adminSite(request)
        _enlatadosproductsfilter.enlatadosProductsFilterAdmin()

        data = _enlatadosproductsfilter.response_data
        data['code'] = _enlatadosproductsfilter.code

        contact_list = data['cantTotal']
        paginator = Paginator(contact_list, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        dataAll = {'contacts':contacts}
        direction = '/static/images/upload/imagesp/'
        return render(request, 'market/adminGestion.html', {'direction':direction,'data':contacts,'flag':'enla'})
    else:
        return render(request, 'market/adminIndex.html', {})

#Caja
def CartOrder(request):
    data = {}
    if str(request.user) != 'AnonymousUser':#si esta logeado su data
        try:
            dataUser = User.objects.get(email=request.user)
            data = {
            'user':dataUser.id,
            'name':dataUser.first_name,
            'email':dataUser.email,
            'apellido':dataUser.last_name,
            'phone':dataUser.user_profile.phone,
            'direction':dataUser.user_profile.direction,
            'rif':dataUser.user_profile.rif,
            'localphone':dataUser.user_profile.localphone,
            'reference':dataUser.user_profile.reference,
            'costoenvio':Tools.objects.get().costoenvio,
            'code':200
            }
        except Exception as e:
            logout(request)
            _allproducts = backStart(request)
            _allproducts.get('all')
            data = _allproducts.response_data
            data['code'] = _allproducts.code
            return render(request, 'market/index.html',{'data':data['data'][0] if data['data'] else {} })

    return render(request, 'market/order.html',data)

#confirmacioncompra
def ConfimationOrder(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, 'market/registerLogin.html', {})
    try:
        dataUser = User.objects.get(email=request.user)
        data = {
        'user':dataUser.id,
        'name':dataUser.first_name,
        'email':dataUser.email,
        'costoenvio':Tools.objects.get().costoenvio,
        'code':200,
        'compra':[],
        'tipoPago':'',
        }
        compra = PurchaseConfirmation.objects.filter(user=dataUser).last()
        allProducts = PurchaseConfirmation.objects.filter(code=compra.code)
        totalGeneral=0
        for value in allProducts:
            data['tipoPago'] = value.payment_type
            data['code'] = value.code
            data['compra'].append({
            'name':value.product.name,
            'price':str(value.product.price)+' / '+str(value.cant_product),
            'image':'/static/images/upload/imagesp/'+value.product.name_image,
            'total':float(value.product.price)*int(value.cant_product),
            })
            totalGeneral = totalGeneral+(float(value.product.price)*int(value.cant_product))

        data['totalGeneral'] = totalGeneral
        data['totalCompleto'] = data['totalGeneral']+data['costoenvio']
        return render(request, 'market/confirmationOrder.html',data)
    except Exception as e:
        print("ConfimationOrder",e)


#envio de formulario de ayuda
def HelpForm(request):
    def hilo():
        try:
            # from django.core.mail import EmailMultiAlternatives
            # from email.mime.image import MIMEImage
            asunto = request.POST.get('asunto')
            email = request.POST.get('email')
            mensaje = request.POST.get('mensaje')
            sendinblue_send('contacto',email,"","",{"asunto":asunto,"mensaje":mensaje})
            # msg_html = render_to_string('market/emailHelp.html',
            # {
            #     "asunto":asunto,
            #     "email":email,
            #     "mensaje":mensaje,
            # })
            #
            # send_mail(
            # asunto,
            # asunto,
            # settings.EMAIL_HOST_USER,#from
            # [request.POST.get('email','')],#to
            # html_message=msg_html,
            # )
            #funciona solo que desde el fron hay problemas al enviar la data
            # html_content = render_to_string('market/emailHelp.html', {
            #     "asunto":asunto,
            #     "email":email,
            #     "mensaje":mensaje,
            # })
            # text_content = render_to_string('market/emailHelp.html', {
            #     "asunto":asunto,
            #     "email":email,
            #     "mensaje":mensaje,
            # })
            # msg = EmailMultiAlternatives(asunto, text_content,
            #                             email,[settings.EMAIL_HOST_USER])
            #
            # msg.attach_alternative(html_content, "text/html")
            #
            # msg.mixed_subtype = 'related'
            # #guardo la imagen del pago##
            # datos = {'picture':request.FILES['image'],'email_user':email}
            # new_pago = PagosImagenes(**datos)
            # new_pago.save()
            # ###########################
            #
            # ruta = str(new_pago.picture)
            # fp = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/static/images/upload/'+ruta, 'rb')
            #
            # msg_img = MIMEImage(fp.read())
            #
            # fp.close()
            # msg_img.add_header('Content-ID', '<{}>'.format(1))
            # msg.attach(msg_img)
            # #envio de email
            # msg.send()
        except Exception as e:
            print(e)

    thread = Thread(target = hilo)
    thread.start()
    data = {'code':200}
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

def CartOrderEntrega(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, 'market/registerLogin.html', {})

    data = {}
    _allproducts = backStart(request)
    _allproducts.guardaCompra()
    data['code'] = _allproducts.code
    if data['code'] !=500:
        data = {'code':200}
    else:
        data = {'code':500,'message':'Error al procesar su compra'}

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

#pagina de recuperacion de clave
def Restore(request):
    return render(request, 'market/restore.html', {})

#envio de recuperacion de clave
def Forgot(request):
    try:
        dataUser = User.objects.get(email=request.POST['email'])
        ########################codigo de seguridad de cambio de clave##########
        def ran_gen(size, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))

        tokenCode = ran_gen(30,"abcdefghijkLmnNopqrstuvwxyz0123456789./*-")
        ########################################################################
        try:
            token = TokenPassword.objects.get(user=dataUser)
            token.token = tokenCode
        except Exception as e:
            dataToke = {'token':tokenCode,'user':dataUser}
            token = TokenPassword(**dataToke)

        token.save()

        def forgotPassword():
            try:

                sendinblue_send('forgot',dataUser.email,"","",{'token':request.build_absolute_uri()+'mail/?token='+dataToke['token']})
                # msg_html = render_to_string('market/forgotPassword.html',
                # {
                # 'email':request.POST.get('email',''),
                # 'token':tokenCode,
                # })
                #
                # send_mail(
                # 'Recuperar Clave',
                # 'siga los pasos',
                # settings.EMAIL_HOST_USER,#from
                # [request.POST.get('email','')],#to
                # html_message=msg_html,
                # )
            except Exception as e:
                print ('e',e)

        thread = Thread(target = forgotPassword)
        thread.start()

        data = {'code':200}
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
    except Exception as e:
        print (e)
        data = {'code':500,'message':'Email no existe'}
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')



def ForgotMail(request):
    if 'token' in request.GET:
        try:
            TokenPassword.objects.get(token=request.GET.get('token'))
            return render(request, 'market/forgotPasswordFinal.html', {'token':request.GET['token']})
        except Exception as e:
            return render(request, 'market/error404.html', {})
    else:
        return render(request, 'market/error404.html', {})

def Detail(request):
    if 'code' in request.GET:
        _detailproducts = backStart(request)
        _detailproducts.detailProducts()
        data = _detailproducts.response_data
        direction = '/static/images/upload/imagesp/'
        return render(request, 'market/detailProduct.html', {'direction':direction,'data':data['data'],'data2':data['data2'][0]})
    else:
        data = {'code':500,'message':'Codigo invalido'}
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

def Register(request):
    return render(request, 'market/register.html', {'flag':1})

def SendEmailClient(request):
    try:
        email = request.POST.get("email")
        if email:
            dataUser = User.objects.get(email=request.POST['email'])
            sendinblue_send('registro',dataUser.email,dataUser.first_name,dataUser.last_name,None)
    except Exception as e:
        pass
