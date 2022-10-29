from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Products
from .models import Category
from .models import Customer
from .models import Orders
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate,logout
from main.middlewares.auth import auth_middleware

# Create your views here.

def index(request):
    if request.method=='POST':
        product=request.POST["product"]
        remove=request.POST.get('remove')
        cart=request.session.get('cart')

        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                else:
                    cart[product]=quantity+1

            else:
                cart[product]=1

        else:
            cart={}
            cart[product]=1
        request.session['cart']=cart
        print('cart',request.session['cart'])
        return redirect('/')

    cart=request.session.get('cart')
    if not cart:
        request.session['cart']={}
    categories=Category.objects.all()
    category_id= request.GET.get('category')
    print(category_id)

    if category_id:
        products=Products.get_all_products_by_category_id(category_id)
    else:

        products=Products.get_all_products();


    data={}
    data['products']=products
    data['categories']=categories
    #print('hello',request.session.get('email'))

    return render(request,'main/index.html',data)



def signup(request):
    if (request.method=="POST"):
        first_name_=request.POST['fname']
        last_name_=request.POST['lname']
        phone_=request.POST['phone']
        email_=request.POST['email']
        password_=request.POST['password']
        print(first_name_)

        customer=Customer(firt_name=first_name_,last_name=last_name_,phone=phone_,email=email_,password=password_)
        customer.password=make_password(customer.password)
        customer.register()
        return redirect('/')

    return render(request,'main/signup.html')

def login(request):
    if (request.method=="POST"):
        email_=request.POST['email']
        password_=request.POST['password']
        customer=Customer.get_customer_by_email(email_)
        print('aaa',customer)

        error_message=None

        if customer:
            flag=check_password(password_,customer.password)
            if flag:
                request.session['customer_id']=customer.id
                request.session['email']=customer.email
                #print('bbb',customer.email)


                return redirect('/')
            else:
                error_message="Email or Password Invalid !!"
        else:
            error_message="Email or Password Invalid !!"
    return render(request,'main/login.html')


def LogoutUser(request):
    logout(request)

    return redirect('/')


def cart(request):
    ids=list(request.session.get('cart').keys())
    products=Products.get_product_by_id(ids)
    print(products)
    return render(request,'main/cart.html',{'products':products})

@auth_middleware
def checkout(request):
    #print(request.POST)
    address=request.POST.get('address')
    phone=request.POST.get('phone')
    customer=request.session.get('customer_id')
    cart=request.session.get('cart')
    products=Products.get_product_by_id(list(cart.keys()))
    print('hi',customer,cart,address,phone)

    for product in products:
        order=Orders(customer=Customer(id=customer),product=product,price=product.price,address=address,phone=phone,quantity=cart.get(str(product.id)))


        #print(order.placeorder());
        order.save()

    request.session['cart']={}

    return redirect('cart')

@auth_middleware
def orders(request):

    #return render(request,'main/orders.html')
    customer=request.session.get('customer_id')
    #print('akash',customer)
    order=Orders.get_orders_by_customer(customer)

    print('thankyou',order)
    return render(request,'main/orders.html',{'order':order})
