from datetime import datetime, timedelta, date, time
import schedule, time, pytz, datetime
from threading import Thread
from maracay import config

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def verificacion_compras():
    def hiloDeChequeo():
        def trabajoRecursivo():
            try:
                print ("mirar que es lo que debo chequear")
                from maracay.models import PurchaseConfirmation, Product
                comprasParaVerificar = PurchaseConfirmation.objects.filter(confirmation=2)
                for compra in comprasParaVerificar:
                    ahora = datetime.datetime.now(pytz.timezone('America/Caracas'))
                    # fechaAcomparar = compra.start_date+timedelta(hours=config.TIEMPO_DE_ANULACION_COMPRA)
                    fechaAcomparar = compra.start_date+timedelta(minutes=1)
                    if ahora>fechaAcomparar:
                        print ('Anular la compra',compra.id)
                        compra.confirmation = 1
                        #restituyo la cantidad de productos comprados
                        producto = Product.objects.get(id=compra.product.id,visible=True)
                        producto.cant = int(producto.cant)+int(compra.cant_product)
                        #guardo cambios
                        compra.save()
                        producto.save()

            except Exception as e:
                raise

        schedule.every(2).minutes.do(trabajoRecursivo)#ponerlo cada 30 minutos
        while True:
            schedule.run_pending()
            time.sleep(1)

    thread = Thread(target = hiloDeChequeo)
    thread.start()


#Agrega costo de envio por defecto
def agrega_costo():
    from maracay.models import Tools
    try:
        costo = Tools.objects.get()
    except Exception as e:
        data = {'costoenvio':config.COSTO_ENVIO,'create_at':datetime.datetime.now()}
        costo = Tools(**data)
        costo.save()
