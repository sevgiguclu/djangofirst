from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from home.models import UserProfile
from order.models import Order, OrderProduct
from product.models import Category, Comment, Product, Images, ProductImageForm
from user.forms import UserUpdateForm, ProfileUpdateForm, ProductForm


@login_required(login_url='/login')  # login durumu kontrol edilir
def index(request):
    category = Category.objects.all()
    current_user = request.user  # kullanıcı oturum bilgileri
    profile = UserProfile.objects.get(user_id=current_user.id)

    context = {'category': category,
               'profile': profile,

               }
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')  # login durumu kontrol edilir
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user kullanıcı verisidir
        # "instance = request.user.userprofile", "userprofile" modelinden gelir -> OneToOneField ilişkisi
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                         instance=request.user.userprofile)  # instance ile bağlıyoruz
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')  # login durumu kontrol edilir
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was succesfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        context = {
            'category': category,
            'form': form,
        }
        return render(request, 'change_password.html', context)


@login_required(login_url='/login')  # login durumu kontrol edilir
def orders(request):
    category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'orders': orders,
    }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')  # login durumu kontrol edilir
def orderdetail(request, id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')  # login durumu kontrol edilir
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # login durumu kontrol edilir
def products(request):
    category = Category.objects.all()
    current_user = request.user
    pro = Product.objects.filter(user_id=current_user.id,)
    # pro = Product.objects.all()
    context = {
        'category': category,
        'products': pro,
    }
    return render(request, 'user_products.html', context)


@login_required(login_url='/login')  # login durumu kontrol edilir
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')  # login durumu kontrol edilir
def user_newproduct(request):
    current_user = request.user
    if request.method == 'POST':  # Form post edildiyse
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            data = Product()  # model ile bağlantı kur
            data.category = form.cleaned_data['category']  # formdan bilgiyi al
            data.user = current_user
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.price = form.cleaned_data['price']
            data.image = form.cleaned_data['image']
            data.amount = form.cleaned_data['amount']
            data.detail = form.cleaned_data['detail']
            data.slug = form.cleaned_data['slug']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Ürününüz başarı ile gönderilmiştir.")
            return HttpResponseRedirect('/user/products')
        else:
            messages.warning(request, "Hata:" + str(form.errors))
            return HttpResponseRedirect('/user/products')

    category = Category.objects.all()
    form = ProductForm()
    context = {'form': form, 'category': category, }
    return render(request, 'user_newproduct.html', context)

@login_required(login_url='/login')  # login durumu kontrol edilir
def edituserproduct(request,id):
    product= Product.objects.get(id=id)
    if request.method == 'POST':  # Form post edildiyse
        form = ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,"Ürün başarıyla güncellendi..")
            return HttpResponseRedirect('/user/products'+ str(id))
        else:
            messages.warning(request, "Hata:" + str(form.errors))
            return HttpResponseRedirect('user/edituserproduct')
    else:
        category = Category.objects.all()
        form = ProductForm(instance=product)#formu doldurup öyle göstericez
        context = {'form': form, 'category': category, }
        return render(request, 'user_newproduct.html', context)

@login_required(login_url='/login')  # login durumu kontrol edilir
def deleteuserproduct(request,id):
    current_user = request.user
    Product.objects.filter(id=id,user_id=current_user.id).delete()
    messages.success(request, "Ürün başarıyla silindi..")
    return HttpResponseRedirect('/user/products')


def productaddimage(request,id):
    if request.method == 'POST':  # Form post edildiyse
        lasturl = request.META.get('HTTP_REFERER')
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.product_id = id
            data.title = form.cleaned_data['title']
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, "Resim başarılı şekilde yüklendi..")
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, "Hata:" + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        product = Product.objects.get(id=id)
        images = Images.objects.filter(product_id=id)
        form = ProductImageForm()
        context = {'product': product,
                   'images': images,
                   'form': form,
                   }
        return render(request,'product_gallery.html',context)