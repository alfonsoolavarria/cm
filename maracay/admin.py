from django.contrib import admin
from .models import (Tools, Profile as ProfileDB, PurchaseConfirmation,
TokenPassword, Product, Shopping, purchaseHistory,DolarBolivar)
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_image', 'price', 'pricebs')
    list_filter = ('name', 'price', 'pricebs')
    search_fields = ('name', 'price', 'pricebs')

admin.site.register(Product,ProductAdmin)
admin.site.register(Tools)
admin.site.register(Shopping)
admin.site.register(PurchaseConfirmation)
admin.site.register(purchaseHistory)

class DolarAdmin(admin.ModelAdmin):
    list_display = ('bolivar',)
admin.site.register(DolarBolivar,DolarAdmin)
