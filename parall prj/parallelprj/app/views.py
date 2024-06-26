
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from . models import Product,Payment,OrderPlaced, Wishlist
from .models import Customer,Cart,Product
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Q
#import razorpay
from django.conf import settings
import requests
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import HttpResponse



# Create your views here.
@login_required
def home(request):
    totalitems = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request,"app/home.html", locals())

@login_required
def about(request):
    totalitems = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request,"app/about.html", locals())

@login_required
def contact(request):
    totalitems = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request,"app/contact.html", locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitems = 0
        wishitem = 0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user=request.user))
            totalitems = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        totalitems = 0
        wishitem = 0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user=request.user))
            totalitems = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category= product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        totalitems = 0
        wishitem = 0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user=request.user))
            totalitems = len(Cart.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        return render(request,"app/productdetail.html",locals())
   
class CustomerRegistrationView(View): 
    def get(self, request):
        totalitems = 0
        wishitem = 0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user=request.user))
            totalitems = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm() 
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        totalitems = 0
        wishitem = 0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user=request.user))
            totalitems = len(Cart.objects.filter(user=request.user))
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register is Successful")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitems = 0
        wishitem = 0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user=request.user))
            totalitems = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html',locals())

    def post(self,request):
        totalitems = 0
        wishitem = 0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user=request.user))
            totalitems = len(Cart.objects.filter(user=request.user))
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode= form.cleaned_data['zipcode']
            reg= Customer(user=user,name=name,locality=locality,mobile=mobile, city=city,state=state,zipcode=zipcode)
         
            reg.save()

            messages.success(request,"Congratulatiobs! Profile is saved Successfully!")
        else:
            messages.warning(request, "Invalid Data!")
        return render(request, 'app/profile.html',locals())

@login_required
def address(request):
    totalitems = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitems = len(Cart.objects.filter(user=request.user))
    add= Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        totalitems = 0
        wishitem = 0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user=request.user))
            totalitems = len(Cart.objects.filter(user=request.user))
        add = Customer.objects.get(pk=pk)
        form= CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())

    def post(self,request,pk):
        totalitems = 0
        wishitem = 0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user=request.user))
            totalitems = len(Cart.objects.filter(user=request.user))
        form= CustomerProfileForm(request.POST)
        if form. is_valid():
            add = Customer.objects.get (pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data[ 'locality']
            add.city = form. cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form. cleaned_data['state']
            add.zipcode = form. cleaned_data['zipcode']
            add.save()

            messages.success (request, "Congratulations ! Profile Update Successfully")
        else:
            messages. warning(request, "Invalid Input Data")
        return redirect("address")

@login_required
def add_to_cart(request) :
    totalitems = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitems = len(Cart.objects.filter(user=request.user))
    user = request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get (id=product_id)
    if Cart.objects.filter(user=user, product=product).exists():
        return redirect("/cart")
    Cart(user=user, product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request) :
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 50
    totalitems = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitems = len(Cart.objects.filter(user=request.user))
    return render (request,'app/addtocart.html',locals ())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    wishlist = Wishlist.objects.filter(user=user)
    return render(request,'app/wishlist.html',locals ())

class checkout(View):
    def get(self,request):
        add = Customer.objects.filter(user=request.user)
        cart_items = Cart.objects.filter(user=request.user)
        amount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 50
        razoramount = int(totalamount*100)
        return render(request, 'app/checkout.html', locals())
    

@login_required
def payment_done(request):
    if request.method == 'POST':
        credit_card = request.POST.get('credit_card')
        user_id = request.POST.get('user_id')      
        # Save payment information
        payment = Payment.objects.create(credit_card=credit_card, user_id=user_id) 
        # Save order details
        user = request.user
        customer = Customer.objects.get(user=user)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced.objects.create(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment)
            c.delete()
        
        return redirect("orders")
    else:
        return redirect("checkout")



@login_required
def orders(request):
    totalitems = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitems = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) # must be a login user
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount+ value
        totalamount = amount + 50
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) # must be a login user
        c.quantity-=1
        c.save()
        cart = Cart.objects.filter(user=request.user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount+ value
        totalamount = amount + 50
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
     if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) # must be a login user
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount+ value
        totalamount = amount + 50
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {'message' : 'Added to Wishlist Successfully'}
        return JsonResponse(data)
@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {'message' : 'Removed from Wishlist Successfully'}
        return JsonResponse(data)
@login_required
def search(request):
    query = request.GET['search']
    totalitems = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitems = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", locals())