from __future__ import absolute_import, unicode_literals
import random
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from celery.decorators import task
from maracay.sendinblue import sendinblue_send
from datetime import datetime
import json,random, string
import base64
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from maracay.models import PagosImagenes, PurchaseConfirmation
from datetime import datetime, timedelta, date, time
import schedule, time, pytz, datetime

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')

@periodic_task(run_every=(crontab(minute='10')),name="verificacion_compras_schedule")
def verificacion_compras_schedule():
    from maracay.models import PurchaseConfirmation, Product
    comprasParaVerificar = PurchaseConfirmation.objects.filter(confirmation=2)
    for compra in comprasParaVerificar:
        ahora = datetime.datetime.now(pytz.timezone('America/Caracas'))
        # fechaAcomparar = compra.start_date+timedelta(hours=config.TIEMPO_DE_ANULACION_COMPRA)
        fechaAcomparar = compra.start_date+timedelta(minutes=1)
        if ahora>fechaAcomparar:
            print ('Anular la compra',compra.id)
            print(compra.product.id)
            compra.confirmation = 1
            #restituyo la cantidad de productos comprados
            producto = Product.objects.get(id=compra.product.id)
            producto.cant = int(producto.cant)+int(compra.cant_product)
            #guardo cambios
            compra.save()
            producto.save()

@app.task()
def forgot_pass(kwargs_):
    sendinblue_send(
        'forgot',
        kwargs_["email"],
        "",
        "",
        {'token':kwargs_["uriab"]+'mail/?token='+kwargs_["token"]}
    )

@app.task()
def help_form(kwargs_):
    try:
        image_data = None

        if kwargs_["imagen"]:
            print("Tengo imagen")
            image_data = kwargs_["imagen"]
            nombre_imagen = kwargs_['nombre_imagen']
            codigo = kwargs_['codigo']
            extension = kwargs_['extension']
        # print('foto',request.FILES.get('foto'))
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d")
        data_imagen_sendinblue = {}
        #guardado del archivo


        def ran_gen(size, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))

        nombre_random = ran_gen(5,"abcdefghijkLmnNopqrstuvwxyz0123456789*")


        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]#otra extension por si acaso
            data = ContentFile(base64.b64decode(imgstr))
            file_name = str(current_time)+"-"+codigo+extension
            localtion_save = settings.MEDIA_ROOT+"/imagesp/capturas/"

            fs = FileSystemStorage(location=localtion_save)
            mymodel = PagosImagenes(email_user=kwargs_["email"],asunto=kwargs_["asunto"],codigo_compra=kwargs_["codigo"],mensaje=kwargs_["mensaje"])

            istan = mymodel.picture.save(file_name,data)

            data_imagen_sendinblue["content"] = kwargs_['origin']+'/static/images/upload/imagesp/capturas/'+file_name
            # data_imagen_sendinblue["content"] = "https://files.realpython.com/media/django-celery.ac2cf9719a6e.png"
            data_imagen_sendinblue["name"] = file_name

        sendinblue_send('contacto',kwargs_["email"],"","",{
            "asunto":kwargs_["asunto"],
            "mensaje":kwargs_["mensaje"],
            "codigo":kwargs_["codigo"] if kwargs_["codigo"] else None,
            "attachment":[data_imagen_sendinblue]
        })
    except Exception as e:
        print("forgot_pass",e)


@app.task()
def send_factura(kwargs_):
    try:
        ###############################
        #Envio la factura por email
        carroEmail = {'compra':[]}
        allProducts = PurchaseConfirmation.objects.filter(code=kwargs_["comprascode"])
        totalGeneral=0
        direction = '/static/images/upload/imagesp/'
        for value in allProducts:
            carroEmail['compra'].append({
            'image':kwargs_["origin"]+direction+value.product.name_image,
            'name':value.product.name,
            'price':str(value.product.price)+' / '+str(value.cant_product),
            'total':float(value.product.price)*int(value.cant_product),
            })
            totalGeneral = totalGeneral+(float(value.product.price)*int(value.cant_product))
        carroEmail['totalGeneral'] = round(totalGeneral,2)
        carroEmail['totalCompleto'] = carroEmail['totalGeneral']+kwargs_["costo_envio"]


        sendinblue_send('detallescompra',str(kwargs_["params_user"]),"","",{
            "asunto":"Factura",
            'payment_type':kwargs_["pago"],
            'email':str(kwargs_["params_user"]),
            'carro':carroEmail['compra'],
            'totalGeneral':round(carroEmail['totalGeneral'],2),
            'totalCompleto':round(carroEmail['totalCompleto'],2),
            'codigo':kwargs_["comprascode"],
            'costoEnvio':kwargs_["costo_envio"],
            'direction':direction,
            'origin':kwargs_["origin"],
        })
    except Exception as e:
        print("send_factura",e)
