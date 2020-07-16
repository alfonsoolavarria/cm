from django.contrib.auth.models import User
from maracay.models import Product, Profile, PurchaseConfirmation, Tools, purchaseHistory
from django.db import transaction
import json,random, string
# from threading import Thread
import threading
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta, date, time
import schedule, time, pytz, datetime
from maracay import verificacion_compras
from maracay.sendinblue import sendinblue_send

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
        try:
            ########################codigo de seguridad de compra###################
            def ran_gen(size, chars=string.ascii_uppercase + string.digits):
                return ''.join(random.choice(chars) for x in range(size))

            tokenCode = ran_gen(11,"abcdefghijkLmnNopqrstuvwxyz0123456789./*-")
            ########################################################################

            carro = json.loads(self._request.POST['carrito'])
            costo_envio = Tools.objects.get(pk=1).costoenvio
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
                    confirmation=2,
                    product=dataSave['product'],
                    start_date=dataSave['start_date'],
                    cant_product=dataSave['cant_product'],
                )
                # dataSave['product'].cant = dataSave['product'].cant - int(dataSave['cant_product'])
                update_product_cant = Product.objects.get(pk=int(dataSave['product'].id))
                update_product_cant.cant= int(update_product_cant.cant) - int(dataSave['cant_product'])
                update_product_cant.save()
                # dataSave['product'].update(cant=dataSave['product'].cant - int(dataSave['cant_product']))
                # dataSave['product'].save()
                compras.save()
                dataSave = {}
                productId = 0
            ####################save historial################
            historialCompras = purchaseHistory.objects.create(
                code_purchase=tokenCode,
                lugarpago=self._request.POST['lugarpago'],
                categoria_pago=self._request.POST['categoria_pago'],
                payment_type=self._request.POST['pago'],
                user=user,
                total=self._request.POST['total'],
                moneda=self._request.POST['moneda'],
            )
            historialCompras.save()
        except Exception as e:
            self.code = 500
            return


        def hilo2(comprascode,pago,params_user,costo_envio):
            try:
                print ("dentro del hilo")
                print("pago",pago)
                print("user",user)
                ###############################
                #Envio la factura por email
                carroEmail = {'compra':[]}
                allProducts = PurchaseConfirmation.objects.filter(code=comprascode)
                totalGeneral=0
                for value in allProducts:
                    carroEmail['compra'].append({
                    'image':value.product.name_image,
                    'name':value.product.name,
                    'price':str(value.product.price)+' / '+str(value.cant_product),
                    'total':float(value.product.price)*int(value.cant_product),
                    })
                    totalGeneral = totalGeneral+(float(value.product.price)*int(value.cant_product))
                carroEmail['totalGeneral'] = totalGeneral
                carroEmail['totalCompleto'] = carroEmail['totalGeneral']+costo_envio
                direction = '/static/images/upload/imagesp/'

                sendinblue_send('detallescompra',str(params_user),"","",{
                    "asunto":"Factura",
                    'payment_type':pago,
                    'email':str(params_user),
                    'carro':carroEmail['compra'],
                    'totalGeneral':carroEmail['totalGeneral'],
                    'totalCompleto':carroEmail['totalCompleto'],
                    'codigo':comprascode,
                    'costoEnvio':costo_envio,
                    'direction':direction,
                })

                # msg_html = render_to_string('market/facturaCompra.html',
                #     {
                #         'asunto':'Factura' ,
                #         'payment_type':self._request.POST['pago'],
                #         'email':self._request.user,
                #         'carro':carroEmail['compra'],
                #         'totalGeneral':carroEmail['totalGeneral'],
                #         'totalCompleto':carroEmail['totalCompleto'],
                #         'codigo':tokenCode,
                #         'costoEnvio':costo_envio,
                #         'direction':direction,
                #     })
                #
                # send_mail(
                #     'Detalles de la Compra',
                #     'Subject',
                #     settings.EMAIL_HOST_USER,#from
                #     [user.email,settings.EMAIL_HOST_USER],#to
                #     html_message=msg_html,
                # )
                #verificar si el hilo de revision de compras esta o no activo
                objeto_tools = Tools.objects.get(pk=1)
                if objeto_tools.hilo_en_proceso == 0:
                    # proceso trabajoRecursivo
                    print("Ejecucion de Hilo")
                    verificacion_compras()
                    objeto_tools.hilo_en_proceso=1
                    objeto_tools.save()
            except Exception as e:
                print ("----",e)
                self.code = 500
                return

        envioemailfactura = threading.Thread(target = hilo2, args=(compras.code,self._request.POST['lugarpago'],self._request.user,costo_envio,))
        envioemailfactura.start()

    def detailProducts(self):
        try:
            history = purchaseHistory.objects.filter(code_purchase=self._request.GET['code'])
            productos = PurchaseConfirmation.objects.filter(code=self._request.GET['code'])
            totalGeneral=0
            moneda = ""
            payment_type = ""
            lugarpago = ""
            for h in history:
                moneda = h.moneda
                payment_type=h.payment_type
                lugarpago=h.lugarpago
                for value in productos:
                    totalGeneral = totalGeneral+(float(value.product.price)*int(value.cant_product))
                    self.response_data['data'].append({
                        'payment_type':h.payment_type,
                        'code':value.code,
                        'confirmation':value.confirmation,
                        'start_date':value.start_date,
                        'name':value.product.name,
                        'price':value.product.price,
                        'image':value.product.name_image,
                        'total':float(value.product.price)*int(value.cant_product),
                        'cant_product':value.cant_product,
                    })

            totalCompleto = totalGeneral+Tools.objects.get(pk=1).costoenvio
            self.response_data['data2'].append({
                'totalGeneral':totalGeneral,
                'totalCompleto':totalCompleto,
                'direccion':Profile.objects.get(user=self._request.user.id).direction,
                'costoenvio':Tools.objects.get(pk=1).costoenvio,
                'moneda':moneda if moneda != "" else "USD" ,
                'payment_type':payment_type if payment_type != "" else "No aplica",
                'lugarpago':lugarpago if lugarpago != "" else "No aplica",
            })
        except Exception as e:
            print("detailProducts",e)


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
            self.code = 409
            return self.response_data['error'].append("Error al crear Usuario/Sin email")

        if 'name' in self._request.POST:
            inssertDict['first_name']=self._request.POST['name']
        if 'lastname' in self._request.POST:
            inssertDict['last_name']=self._request.POST['lastname']

        if 'password' in self._request.POST:
            inssertDict['password'] = self._request.POST['password']
        else:
            self.code = 409
            return self.response_data['error'].append("Error al crear Usuario/Sin contraseña")

        if 'phone' in self._request.POST:
            inssertDictProfile['phone'] = self._request.POST['phone']
        else:
            self.code = 409
            return self.response_data['error'].append("Debe insertar un número célular")

        if 'direction' in self._request.POST:
            inssertDictProfile['direction'] = self._request.POST['direction']
        else:
            self.code = 409
            return self.response_data['error'].append("Debe insertar una Dirección")
        try:
            with transaction.atomic():
                try:
                    getVerifiedUser = User.objects.get(username=inssertDict['username'])
                    self.code = 500
                    return self.response_data['error'].append("Intente con otro email")
                except Exception as e:
                    user = User.objects.create_user(**inssertDict)
                    inssertDictProfile['user'] = user
                    creteProfile = Profile(**inssertDictProfile)
                    creteProfile.save()
                    print("save user")
        except Exception as e:
            print ("Error al guardar usuario",e)
            self.code = 500
            return self.response_data['error'].append("Error al crear Usuario"+str(e))


    def accountData(self):
        try:
            dataA = purchaseHistory.objects.filter(user=self._request.user)[:35]
            for a in dataA:
                tabladecompra = PurchaseConfirmation.objects.filter(code=a.code_purchase).last()
                if tabladecompra:
                    self.response_data['data'].append({
                    "code_purchase":a.code_purchase,
                    # "total":(tabladecompra.cant_product*tabladecompra.product.price)+Tools.objects.get(pk=1).costoenvio,
                    "total":a.total,
                    "state":tabladecompra.confirmation,
                    "payment_type":a.payment_type+"-"+a.moneda,
                    "start_date":tabladecompra.start_date-timedelta(hours=4),
                    })
        except Exception as e:
            print("account",e)





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
    def charcuteriaProductsFilter(self):
        self.response_data['cantTotal']= Product.objects.filter(category=4)
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
    def carnesProductsFilter(self):
        self.response_data['cantTotal']= Product.objects.filter(category=5)
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

    def allProductsTable(self):
        print("----???legueee")
        for a in Product.objects.all():
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            "price":float(a.price),
            "pricebs":float(a.pricebs)
            })

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
