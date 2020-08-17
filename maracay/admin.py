from django.contrib import admin
from .models import (Tools, Profile as ProfileDB, PurchaseConfirmation,
TokenPassword, Product, Shopping, purchaseHistory,DolarBolivar, PagosImagenes)
from django.utils.html import format_html

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','name_image', 'price', 'pricebs','visible')
    list_filter = ('name', 'price', 'pricebs')
    search_fields = ('name', 'price', 'pricebs')

class Model1Admin(admin.ModelAdmin):
    list_display = ('codigo_compra','create_at',)
    fields = ['image_tag','asunto','codigo_compra','mensaje','create_at']
    readonly_fields = ['image_tag','asunto','codigo_compra','mensaje','create_at']

class DolarAdmin(admin.ModelAdmin):
    list_display = ('bolivar',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Tools)
admin.site.register(Shopping)
admin.site.register(PurchaseConfirmation)
admin.site.register(purchaseHistory)
admin.site.register(DolarBolivar,DolarAdmin)
admin.site.register(PagosImagenes,Model1Admin)
