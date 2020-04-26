from django.contrib.auth.models import User
from maracay.models import Product, Profile, PurchaseConfirmation, Tools, purchaseHistory
from django.db import transaction
import json,random, string
from threading import Thread
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta, date, time
import schedule, time, pytz, datetime


class backStart():
    def __init__(self, request):
        self._request = request
        self.user = 0
        self.response_data = {'error':[], 'data':[],'data2':[]}
        self.code = 200

    def get(self,params=None):
        self.response_data['cantTotal']= Product.objects.all()
        #self.response_data['first'] = self._request.GET.get('start',0)
        #self.response_data['last'] = self._request.GET.get('end',12)

        try:
            for a in Product.objects.all():
                self.response_data['data'].append({
                "category":a.category,
                "id":a.id,
                "name":a.name,
                "cant":a.cant,
                "description":a.description,
                "name_image":a.name_image,
                #"price":a.price,
                })
            '''for b in Product.objects.filter()[int(self._request.GET.get('start',0)):int(self._request.GET.get('end',12))]:
                self.response_data['data2'].append({
                "category":b.category,
                "id":b.id,
                "cant":b.cant,
                "name":b.name,
                "description":b.description,
                "image":b.image,
                #"price":b.price,
                })'''
        except Exception as e:
            self.code = 500
            return self.response_data['error'].append(str(e))

    def guardaCompra(self):
        def hilo2():
            try:
                print (self._request.POST)
                ########################codigo de seguridad de compra###################
                def ran_gen(size, chars=string.ascii_uppercase + string.digits):
                    return ''.join(random.choice(chars) for x in range(size))

                tokenCode = ran_gen(30,"abcdefghijkLmnNopqrstuvwxyz0123456789./*-")
                ########################################################################

                carro = json.loads(self._request.POST['carrito'])

                dataSave = {}
                productId = 0
                carroEmail = {'compra':[]}
                for value in carro:
                    for k,v in value.items():
                        if k == 'id':
                            dataSave['product']=Product.objects.get(pk=int(v))
                        if k == 'cantidad':
                            dataSave['cant_product']=v

                    dataSave['start_date'] = self._request.POST['start_date']
                    dataSave['code'] = tokenCode
                    user = User.objects.get(email=self._request.user)
                    compras = PurchaseConfirmation.objects.create(
                        code=dataSave['code'],
                        user=user,
                        payment_type=self._request.POST['pago'],
                        confirmation=2,
                        product=dataSave['product'],
                        start_date=dataSave['start_date'],
                        cant_product=dataSave['cant_product'],
                    )
                    dataSave['product'].cant = dataSave['product'].cant - int(dataSave['cant_product'])
                    dataSave['product'].save()
                    compras.save()
                    dataSave = {}
                    productId = 0

                #save historial################
                historialCompras = purchaseHistory.objects.create(
                    code_purchase=tokenCode,
                    user=user,
                    total=''
                )
                historialCompras.save()
                ###############################
                #Envio la factura por email
                carroEmail = {'compra':[]}
                allProducts = PurchaseConfirmation.objects.filter(code=compras.code)
                totalGeneral=0
                for value in allProducts:
                    carroEmail['compra'].append({
                    'image':value.product.image,
                    'name':value.product.name,
                    'price':str(value.product.price)+' / '+str(value.cant_product),
                    'total':float(value.product.price)*int(value.cant_product),
                    })
                    totalGeneral = totalGeneral+(float(value.product.price)*int(value.cant_product))
                carroEmail['totalGeneral'] = totalGeneral
                carroEmail['totalCompleto'] = carroEmail['totalGeneral']+Tools.objects.get(pk=1).costoenvio

                msg_html = render_to_string('market/facturaCompra.html',
                    {
                        'asunto':'Factura' ,
                        'payment_type':self._request.POST['pago'],
                        'email':self._request.user,
                        'carro':carroEmail['compra'],
                        'totalGeneral':carroEmail['totalGeneral'],
                        'totalCompleto':carroEmail['totalCompleto'],
                        'codigo':tokenCode,
                        'costoEnvio':Tools.objects.get(pk=1).costoenvio,
                    })

                send_mail(
                    'Title',
                    'Subject',
                    settings.EMAIL_HOST_USER,#from
                    ['alfonsojn15@gmail.com'],#to
                    html_message=msg_html,
                )
            except Exception as e:
                print (e)
                self.code = 500

        thread = Thread(target = hilo2)
        thread.start()

    def detailProducts(self):
        print (self._request.user.id)
        productos = PurchaseConfirmation.objects.filter(code=self._request.GET['code'])
        totalGeneral=0
        for value in productos:
            totalGeneral = totalGeneral+(float(value.product.price)*int(value.cant_product))
            self.response_data['data'].append({
                'payment_type':value.payment_type,
                'code':value.code,
                'confirmation':value.confirmation,
                'start_date':value.start_date,
                'name':value.product.name,
                'price':value.product.price,
                'image':value.product.image,
                'total':float(value.product.price)*int(value.cant_product),
                'cant_product':value.cant_product,
            })

        totalCompleto = totalGeneral+Tools.objects.get(pk=1).costoenvio
        self.response_data['data2'].append({
            'totalGeneral':totalGeneral,
            'totalCompleto':totalCompleto,
            'direccion':Profile.objects.get(user=self._request.user.id).direction,
            'costoenvio':Tools.objects.get(pk=1).costoenvio,
        })

class profileBackend():
    def __init__(self, request):
        self._request = request
        self.user = 0
        self.response_data = {'error':[], 'data':[]}
        self.code = 200

    def post(self):
        #creacion de Usuario
        inssertDict = {}
        inssertDictProfile = {}
        if 'email' in self._request.POST:
            inssertDict['email'] = self._request.POST['email']
            inssertDict['username'] = self._request.POST['email']
        else:
            return self.response_data['error'].append("Error al crear Usuario/Sin email")

        if 'name' in self._request.POST:
            inssertDict['first_name']=self._request.POST['name']
        if 'lastname' in self._request.POST:
            inssertDict['last_name']=self._request.POST['lastname']

        if 'password' in self._request.POST:
            inssertDict['password'] = self._request.POST['password']
        else:
            return self.response_data['error'].append("Error al crear Usuario/Sin contraseña")

        if 'phone' in self._request.POST:
            inssertDictProfile['phone'] = self._request.POST['phone']
        else:
            return self.response_data['error'].append("Debe insertar un número célular")

        if 'direction' in self._request.POST:
            inssertDictProfile['direction'] = self._request.POST['direction']
        else:
            return self.response_data['error'].append("Debe insertar una Dirección")

        if 'rif' in self._request.POST:
            inssertDictProfile['rif'] = self._request.POST['rif']
        else:
            inssertDictProfile['rif'] = ''

        if 'localphone' in self._request.POST:
            inssertDictProfile['localphone'] = self._request.POST['localphone']
        else:
            inssertDictProfile['localphone'] = ''

        if 'reference' in self._request.POST:
            inssertDictProfile['reference'] = self._request.POST['reference']
        else:
            inssertDictProfile['reference'] = ''

        try:
            with transaction.atomic():
                try:
                    getVerifiedUser = User.objects.get(username=inssertDict['username'])
                    self.code = 500
                    return self.response_data['error'].append("Ya este Email existe")
                except Exception as e:
                    user = User.objects.create_user(**inssertDict)
                    inssertDictProfile['user'] = user
                    creteProfile = Profile(**inssertDictProfile)
                    creteProfile.save()
        except Exception as e:
            print (e)
            self.code = 500
            return self.response_data['error'].append("Error al crear Usuario"+str(e))


    def accountData(self):
        dataA = purchaseHistory.objects.all()
        for a in dataA:
            tabladecompra = PurchaseConfirmation.objects.filter(code=a.code_purchase).last()
            self.response_data['data'].append({
            "code_purchase":a.code_purchase,
            "total":a.total,
            "state":tabladecompra.confirmation,
            "payment_type":tabladecompra.payment_type,
            "start_date":tabladecompra.start_date-timedelta(hours=4),
            })




class filterProducts():
    def __init__(self, request):
        self._request = request
        self.user = 0
        self.response_data = {'error':[], 'data':[]}
        self.code = 200

    def allProductsFilter(self):
        self.response_data['cantTotal']= Product.objects.all()
        for a in Product.objects.all():
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            #"price":a.price,
            })

    def viveresProductsFilter(self):
        self.response_data['cantTotal']= Product.objects.filter(category=1)
        for a in Product.objects.filter(category=1):
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            #"price":a.price,
            })
    def frigorificoProductsFilter(self):
        self.response_data['cantTotal']= Product.objects.filter(category=2)
        for a in Product.objects.filter(category=2):
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            #"price":a.price,
            })
    def enlatadosProductsFilter(self):
        self.response_data['cantTotal']= Product.objects.filter(category=3)
        for a in Product.objects.filter(category=3):
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            #"price":a.price,
            })

class adminSite():
    def __init__(self, request):
        self._request = request
        self.user = 0
        self.response_data = {'error':[], 'data':[]}
        self.code = 200

    def dataProductUser(self):
        self.response_data['cantTotal']= Product.objects.all()
        for a in Product.objects.all():
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            #"price":a.price,
            })

    def viveresProductsFilterAdmin(self):
        self.response_data['cantTotal']= Product.objects.filter(category=1)
        for a in Product.objects.filter(category=1):
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            #"price":a.price,
            })
    def frigorificoProductsFilterAdmin(self):
        self.response_data['cantTotal']= Product.objects.filter(category=2)
        for a in Product.objects.filter(category=2):
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            #"price":a.price,
            })
    def enlatadosProductsFilterAdmin(self):
        self.response_data['cantTotal']= Product.objects.filter(category=3)
        for a in Product.objects.filter(category=3):
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            #"price":a.price,
            })
