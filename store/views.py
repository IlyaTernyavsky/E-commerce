from datetime import datetime
from http.client import HTTP_PORT
from multiprocessing.sharedctypes import Value
from xml.dom import ValidationErr
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponseRedirect
from store.models import *
import json
from django.contrib.auth import authenticate, login, logout
from cloudipsp import Api, Checkout


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_card_total':0,
                 'get_card_items':0,
                 'shipping':False}
        try:
            cartItems = order['get_cart_items']
        except:
            cartItems = order
    products = Product.objects.all()
    context = {'products':products,'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
            print('Cart:',cart)
        items = []
        order = {'get_card_total':0,
                 'get_card_items':0,
                 'shipping':False}
        cartItems = order['get_cart_items']
        for i in cart:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price + cart[i]['quantity'])

            order['get_cart_total'] += total        
            order['get_cart_total'] += cart[i]['quantity']        
        
    context = {'items':items,'order':order}
    
    return render(request,'store/cart.html',context)




def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all() 
    else:
        items = []
        order = {'get_card_total':0,
                 'get_card_items':0,
                 'shipping': False}


    context = {'items':items,'order':order}


    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)
    
	

def processOrder(request):
	transaction_id = datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAdress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	else:
		print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)


def login_view(request):
    username  = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return redirect('store')
    return render(request,'store/login.html')
    

def logout_view(request):
    logout(request)
    return redirect('store')


    

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        
        on = authenticate(username=username,password=password1)
        if on is not None:
            return redirect('login')
        else:
            user = User(username=username,email=email,password=password1)
            user.save()
            return redirect('login')
            

    
        
        
    return render(request,'store/registration.html')


    
    

    
    
       
        



    

    
