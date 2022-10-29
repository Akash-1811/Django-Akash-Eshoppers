from django.db import models
import datetime

# Create your models here.
class Products(models.Model):
    name=models.CharField(max_length=20)
    price=models.IntegerField()
    category=models.ForeignKey('Category', on_delete=models.CASCADE,null=True, blank=True)
    description=models.TextField()
    image=models.ImageField(upload_to='product/')

    def __str__(self):
        return str(self.name)

    @staticmethod
    def get_product_by_id(ids):
        return Products.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products();

class Category(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class Customer(models.Model):
    firt_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    phone=models.CharField(max_length=15)
    email=models.EmailField()
    password=models.CharField(max_length=100)

    def __str__(self):
        return str(self.firt_name)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.CharField(max_length=200,default='',blank=True)
    phone=models.CharField(max_length=20,default='',blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)

    #def placeorder(self):
    #    self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Orders.objects.filter(customer=customer_id).order_by('-date')
