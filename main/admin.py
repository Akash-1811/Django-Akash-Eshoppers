from django.contrib import admin
from .models import Products
from .models import Category
from .models import Customer
from .models import Orders

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','description','image']

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']

class CustomerAdmin(admin.ModelAdmin):
    list_display=['firt_name','last_name','phone','email','password']

class OrderAdmin(admin.ModelAdmin):
    list_display=['product','customer','quantity','price','date']


admin.site.register(Products,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Orders,OrderAdmin)

# Register your models here.
