from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import mark_safe

# Create your models here.
class Product(models.Model):
    __cate=((1,_('Viveres')),(2,_('Frigorifico')),(3,_('Enlatados')),(4,_('Charcuteria')),(5,_('Carnes')),(6,_('Personales')),(7,_('Chucherias')))
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=1000,help_text="Alias de la imagen")
    price=models.DecimalField(max_digits=30, decimal_places=2,help_text="Precio en Dolares")
    pricebs=models.DecimalField(max_digits=30, decimal_places=2,default=1,help_text="Precion en Bolivares")
    description=models.CharField(max_length=200,help_text="Descripcion del producto")
    name_image=models.CharField(max_length=50,help_text="Debes colocar el nombre de la imagen con la extension por ejemplo: imagen.png ")
    picture = models.ImageField(upload_to='imagesp')
    cant=models.PositiveSmallIntegerField(default=1,help_text="Cantidad disponible el producto en el almacen")
    category=models.PositiveSmallIntegerField(choices=__cate,help_text="Seleccione una categoria del producto")
    visible = models.BooleanField(default=False)
    create_at=models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        verbose_name_plural = "Productos"


class Profile(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User, related_name='user_profile',on_delete=models.CASCADE)
    phone=models.CharField(max_length=50)
    direction=models.CharField(max_length=200)
    tw=models.CharField(max_length=50,null=True)
    fb=models.CharField(max_length=50,null=True)
    google=models.CharField(max_length=50,null=True)
    rif=models.CharField(max_length=50)
    localphone=models.CharField(max_length=50,null=True)
    reference=models.CharField(max_length=200,null=True)
    costoenvio=models.PositiveSmallIntegerField(default=2)
    class Meta:
        verbose_name_plural = "Perfil de Usuario"

class Tools(models.Model):
    id=models.AutoField(primary_key=True)
    hilo_en_proceso=models.PositiveSmallIntegerField(default=0)#0no esta corriendo  1 ya esta iniciado
    create_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Herramientas"

class TokenPassword(models.Model):
    id=models.AutoField(primary_key=True)
    token=models.CharField(max_length=200)
    user=models.ForeignKey(User,related_name='user_token',on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Token Password"

class Shopping(models.Model):#compra
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User, related_name='user_shopping',on_delete=models.CASCADE)
    product=models.OneToOneField(Product, related_name='user_products',on_delete=models.CASCADE)
    cantshopping=models.PositiveSmallIntegerField(default=0)
    code=models.CharField(max_length=1000)
    create_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Compras"

class PurchaseConfirmation(models.Model):#confirmacion de compra
    # __confirmCompra=((1,_('Anulada')),(2,_('Pendiente')),(3,_('Confirmada')))
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,related_name='user_confirm',on_delete=models.CASCADE)
    code=models.CharField(max_length=1000)#codigo de seguridad de la compra
    confirmation=models.PositiveSmallIntegerField(default=2)#para saber si se hizo o no la transferencia
    start_date=models.DateTimeField(null=True)#fecha de creacion sera para el servicio init
    product=models.ForeignKey(Product, related_name='product_comprado',on_delete=models.CASCADE)
    cant_product=models.PositiveSmallIntegerField(default=1)
    create_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Confirmacion de compras"

class purchaseHistory(models.Model):
    #se guarda el historial de compra con su total en la modena que pagara o pago
    id=models.AutoField(primary_key=True)
    code_purchase=models.CharField(max_length=1000)#codigo de seguridad de la compra relacionado a la compra
    total=models.CharField(max_length=1000)#total de compra
    user=models.ForeignKey(User,related_name='user_history',on_delete=models.CASCADE)#usuario que compro
    lugarpago=models.CharField(max_length=1000)#lugar de pago (pais)
    categoria_pago=models.CharField(max_length=1000)#tipo de pago (Nacional o Internacional)
    payment_type=models.CharField(max_length=1000)#modo de pago (PayPal o Transferencia)
    moneda=models.CharField(max_length=1000)#moneda en que cotizo su pago
    create_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Historial de Compras"

class PagosImagenes(models.Model):
    id=models.AutoField(primary_key=True)
    email_user=models.CharField(max_length=200)
    picture = models.ImageField(upload_to='imagesp/capturas/')
    create_at=models.DateTimeField(auto_now_add=True,null=True)
    asunto=models.CharField(max_length=1000)
    codigo_compra=models.CharField(max_length=200)
    mensaje=models.CharField(max_length=1000)
    def image_tag(self):
        return mark_safe('<img src="/static/images/upload/%s" width="150" height="150" />' % (self.picture))
    image_tag.short_description = 'Image'
    class Meta:
        verbose_name_plural = "Imagenes de Pago"

class DolarBolivar(models.Model):
    id=models.AutoField(primary_key=True)
    bolivar=models.DecimalField(max_digits=30, decimal_places=2,help_text="Cambia el dolar al precio actual y todos los precios de los productos en bolivares cambiaran al instante")
    class Meta:
        verbose_name_plural = "Tasa DolarBolivar"

@receiver(post_save, sender=DolarBolivar, dispatch_uid="update_bolivares_product")
def update_bolivares_product(sender, instance, **kwargs):
    update_ = Product.objects.all()
    for value in update_:
        value.pricebs = instance.bolivar
        value.pricebs = value.price*instance.bolivar
        value.save()
