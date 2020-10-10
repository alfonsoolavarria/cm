from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
from maracay.sendinblue import sendinblue_send
from datetime import datetime
import json,random, string
import base64
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from maracay.models import PagosImagenes

@task()
def forgot_pass(kwargs_):
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
