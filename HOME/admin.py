from django.contrib import admin
from .models import *

class cartsearch(admin.ModelAdmin):
    search_fields=['orderid']

class orderdes_search(admin.ModelAdmin):
    search_fields=['complete']

class product_search(admin.ModelAdmin):
    search_fields=['product_id']

class transid_search(admin.ModelAdmin):
    search_fields=['trans_id']
# Register your models here.

admin.site.register(product)
admin.site.register(customer)
admin.site.register(address)
admin.site.register(cartitem,cartsearch)
admin.site.register(orderdescription,orderdes_search)
admin.site.register(order,transid_search)
admin.site.register(message)