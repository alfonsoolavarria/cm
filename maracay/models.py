from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Product(models.Model):
    __cate=((1,_('Viveres')),(2,_('Frigorifico')),(3,_('Enlatados')))
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=30, decimal_places=2)
    description=models.CharField(max_length=200)
    name_image=models.CharField(max_length=50)
    picture = models.ImageField(upload_to='imagesp')
    cant=models.PositiveSmallIntegerField(default=1)
    category=models.PositiveSmallIntegerField(choices=__cate)
    create_at=models.DateTimeField(auto_now_add=True,null=True)

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

class Tools(models.Model):
    id=models.AutoField(primary_key=True)
    costoenvio=models.PositiveSmallIntegerField(default=100)
    create_at=models.DateTimeField(auto_now_add=True)

class TokenPassword(models.Model):
    id=models.AutoField(primary_key=True)
    token=models.CharField(max_length=200)
    user=models.ForeignKey(User,related_name='user_token',on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)

class Shopping(models.Model):#compra
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User, related_name='user_shopping',on_delete=models.CASCADE)
    product=models.OneToOneField(Product, related_name='user_products',on_delete=models.CASCADE)
    cantshopping=models.PositiveSmallIntegerField(default=0)
    code=models.CharField(max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)

class PurchaseConfirmation(models.Model):#confirmacion de compra
    # __confirmCompra=((1,_('Anulada')),(2,_('Pendiente')),(3,_('Confirmada')))
    id=models.AutoField(primary_key=True)
    payment_type=models.CharField(max_length=100)
    user=models.ForeignKey(User,related_name='user_confirm',on_delete=models.CASCADE)
    code=models.CharField(max_length=100)#codigo de seguridad de la compra
    confirmation=models.PositiveSmallIntegerField(default=2)#para saber si se hizo o no la transferencia
    start_date=models.DateTimeField(null=True)#fecha de creacion sera para el servicio init
    product=models.ForeignKey(Product, related_name='product_comprado',on_delete=models.CASCADE)
    cant_product=models.PositiveSmallIntegerField(default=1)
    create_at=models.DateTimeField(auto_now_add=True)

class purchaseHistory(models.Model):
    id=models.AutoField(primary_key=True)
    code_purchase=models.CharField(max_length=100)#codigo de seguridad de la compra relacionado a la compra
    total=models.CharField(max_length=100)
    user=models.ForeignKey(User,related_name='user_history',on_delete=models.CASCADE)
