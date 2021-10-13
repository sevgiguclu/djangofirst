from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import UserProfile
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product


def index(request):
    return HttpResponse("Order App")

@login_required(login_url='/login') #login durumu kontrol edilir
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER')#urli alır
    current_user = request.user #Access User Session Information

    checkproduct = ShopCart.objects.filter(product_id = id)
    if checkproduct:
        control = 1 #ürün sepette var
    else:
        control = 0

    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid:
            if control==1:#ürün varsa güncelle
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request,"Ürün başarı ile sepete eklenmiştir.Teşekkür Ederiz..")
        return HttpResponseRedirect(url)

    else:#sepete ekleye basılınca
        if control == 1:  # ürün varsa güncelle
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart() #model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
            request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
            messages.success(request,"Ürün başarı ile sepete eklenmiştir.Teşekkür Ederiz..")
            return HttpResponseRedirect(url)

    messages.warning(request,"Ürün sepete eklemede hata oluştu! Lütfen kontrol ediniz...")
    return HttpResponseRedirect(url)

@login_required(login_url='/login') #login durumu kontrol edilir
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session Information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()

    total =0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    context = {'shopcart':shopcart,
               'category':category,
               'total':total,
               }
    return render(request,'Shopcart_products.html',context)

@login_required(login_url='/login') #login durumu kontrol edilir
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request,"Ürün Sepetten Silindi...")
    return HttpResponseRedirect("/shopcart"),

@login_required(login_url='/login') #login durumu kontrol edilir
def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user #Access User Session Information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():#kredi kartı bilgilerini bankaya gönder onay gelince devam et
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()#random kod üretir,5 rakamlı, upper ->büyük harfle
            data.code = ordercode
            data.save()


            # Shopcart öğelerini Ürün  sipariş öğelerine taşıma
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()

                #**Ürün Miktarından satılan ürün miktarını azaltın **
                product = Product.objects.get(id = rs.product_id)
                product.amount -= rs.quantity
                product.save()



            ShopCart.objects.filter(user_id=current_user.id).delete()#sepet temizlenir
            request.session['cart_items'] = 0#sepet ürün sayısı sıfırlanır
            messages.success(request,"Your Order has been completed. Thank You ..")
            return render(request,'Order_Completed.html',{'ordercode': ordercode,'category':category})
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect("/order/orderproduct")
    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart':shopcart,
               'category':category,
               'total':total,
               'form':form,
               'profile':profile,
              }
    return render(request,'Order_Form.html',context)





