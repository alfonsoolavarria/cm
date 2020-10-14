from django.contrib.auth.models import User
from maracay.models import Product, Profile, PurchaseConfirmation, Tools, purchaseHistory, DolarBolivar
from django.db import transaction
import json,random, string
# from threading import Thread
import threading
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta, date, time
import schedule, time, pytz, datetime
from maracay import verificacion_compras, formatoBolivares
from maracay.sendinblue import sendinblue_send
from maracay.task import send_factura



class backStart():
    def __init__(self, request):
        self._request = request
        self.user = 0
        self.response_data = {'error':[], 'data':[],'data2':[]}
        self.code = 200

    def get(self,params=None):
        self.response_data['cantTotal']= Product.objects.filter(visible=True)
        #self.response_data['first'] = self._request.GET.get('start',0)
        #self.response_data['last'] = self._request.GET.get('end',12)

        try:
            for a in Product.objects.filter(visible=True):
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
            ####scraping currency from Google
            try:
                valores_conversion = []
                valor_str = ""
                valor_float = ""
                if self._request.POST['categoria_pago']=='Internacional':
                    import requests
                    from bs4 import BeautifulSoup
                    if self._request.POST['lugarpago'] not in ['Paypal','USA','Argentina']:
                        r = requests.get("https://www.google.com/search?q="+self._request.POST['total']+"+usd+to+"+self._request.POST['moneda']+"")
                        soup = BeautifulSoup(r.text, 'html.parser')

                        get_class_value_convert = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

                        for index,value_convert in enumerate(get_class_value_convert):
                            valores_conversion.append(value_convert.text.strip())


                        if valores_conversion:
                            valor_str = valores_conversion[0].split()[0]
                            valor_float=valor_str.replace(",","")
                        else:
                            print("error conversion",e)
                            self.code = 500
                            return

                        # print ("Toma valor en bruto",valor_str)
                        # print ("Total mejorado para save sin el 5%",valor_float)
                        #aumento del 5%, sumo 1 porque el round si es menor de 5 lo deja si es > 5 lo sube
                        # print(type(valor_float),valor_float)
                        #el ,2 despues son la cantidad de decimales a mostrar
                        valor_float=round(float(valor_float)+0.1,2)
                        # print("valor_float",valor_float)
                        aument1 = (valor_float*5)/100
                        valor_float=round(valor_float+aument1,2)
                        # print("--->valor con el 5%",valor_float)
                    else:
                        valor_float=self._request.POST['total']
                        # print ("Total mejorado para save sin el 5% PaypalUSA",valor_float)
                else:
                    # print("Pago Nacional")
                    bolivar_acutal = DolarBolivar.objects.get().bolivar
                    valor_float = round(float(self._request.POST['total'])*float(bolivar_acutal),3)
                    # print("valor_floa--->t",valor_float)
            except Exception as e:
                print("scraping",e)
                self.code = 500
                return
            ####

            ########################codigo de seguridad de compra###################
            def ran_gen(size, chars=string.ascii_uppercase + string.digits):
                return ''.join(random.choice(chars) for x in range(size))

            tokenCode = ran_gen(11,"abcdefghijkLmnNopqrstuvwxyz0123456789*")
            ########################################################################
            user = Profile.objects.get(user__email=self._request.user)

            carro = json.loads(self._request.POST['carrito'])


            costo_envio = int(self._request.POST['costoenvio'])
            user.costoenvio = costo_envio
            user.save()
            dataSave = {}
            productId = 0
            carroEmail = {'compra':[]}
            for value in carro:
                for k,v in value.items():
                    if k == 'id':
                        dataSave['product']=Product.objects.get(pk=int(v),visible=True)
                    if k == 'cantidad':
                        dataSave['cant_product']=v

                dataSave['start_date'] = self._request.POST['start_date']
                dataSave['code'] = tokenCode


                compras = PurchaseConfirmation.objects.create(
                    code=dataSave['code'],
                    user=user.user,
                    confirmation=2,
                    product=dataSave['product'],
                    start_date=dataSave['start_date'],
                    cant_product=dataSave['cant_product'],
                )
                # dataSave['product'].cant = dataSave['product'].cant - int(dataSave['cant_product'])
                update_product_cant = Product.objects.get(visible=True,pk=int(dataSave['product'].id))
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
                user=user.user,
                total=valor_float,
                moneda=self._request.POST['moneda'] if 'moneda' in self._request.POST else "",
            )
            historialCompras.save()

            kwargs_ = {
                "costo_envio":costo_envio,
                "params_user":str(self._request.user),
                "comprascode":compras.code,
                "pago":self._request.POST['lugarpago']}
            envio_email_factura = send_factura.delay(kwargs_)
        except Exception as e:
            print("save",e)
            self.code = 500
            return

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
                if moneda == "Bs":
                    totalcompra = formatoBolivares(None,h.total)
                else:
                    totalcompra=h.total
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

            # totalCompleto = totalGeneral+Tools.objects.get(pk=1).costoenvio
            profile = Profile.objects.get(user=self._request.user.id)
            self.response_data['data2'].append({
                'totalGeneral':totalGeneral,
                'totalCompleto':totalcompra,
                'direccion':profile.direction,
                'costoenvio':profile.costoenvio,
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
            dataA = purchaseHistory.objects.filter(user=self._request.user).order_by('-id')[:35]
            for a in dataA:
                tabladecompra = PurchaseConfirmation.objects.filter(code=a.code_purchase).last()
                if tabladecompra:
                    if a.moneda == "Bs":
                        total="{:,.2f}".format(float(a.total)).replace(","," ")
                        total=total.replace(".",",")
                        total=total.replace(" ",".")
                    else:
                        total=a.total
                    self.response_data['data'].append({
                    "code_purchase":a.code_purchase,
                    # "total":(tabladecompra.cant_product*tabladecompra.product.price)+Tools.objects.get(pk=1).costoenvio,
                    "total":total,
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
        self.response_data['cantTotal']= Product.objects.filter(visible=True)
        for a in Product.objects.filter(visible=True):
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
        self.response_data['cantTotal']= Product.objects.filter(category=1,visible=True)
        for a in Product.objects.filter(category=1,visible=True):
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
        self.response_data['cantTotal']= Product.objects.filter(category=2,visible=True)
        for a in Product.objects.filter(category=2,visible=True):
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
        self.response_data['cantTotal']= Product.objects.filter(category=3,visible=True)
        for a in Product.objects.filter(category=3,visible=True):
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
        self.response_data['cantTotal']= Product.objects.filter(category=4,visible=True)
        for a in Product.objects.filter(category=4,visible=True):
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
        self.response_data['cantTotal']= Product.objects.filter(category=5,visible=True)
        for a in Product.objects.filter(category=5,visible=True):
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            #"price":a.price,
            })
    def personalesProductsFilter(self):
        self.response_data['cantTotal']= Product.objects.filter(category=6,visible=True)
        for a in Product.objects.filter(category=6,visible=True):
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
        for a in Product.objects.filter(visible=True):
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
        self.response_data['cantTotal']= Product.objects.filter(visible=True)
        for a in Product.objects.filter(visible=True):
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            "price":a.price,
            })

    def viveresProductsFilterAdmin(self):
        self.response_data['cantTotal']= Product.objects.filter(category=1,visible=True)
        for a in Product.objects.filter(category=1,visible=True):
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
        self.response_data['cantTotal']= Product.objects.filter(category=2,visible=True)
        for a in Product.objects.filter(category=2,visible=True):
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
        self.response_data['cantTotal']= Product.objects.filter(category=3,visible=True)
        for a in Product.objects.filter(category=3,visible=True):
            self.response_data['data'].append({
            "category":a.category,
            "id":a.id,
            "name":a.name,
            "cant":a.cant,
            "description":a.description,
            "name_image":a.name_image,
            #"price":a.price,
            })
