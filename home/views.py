import json
from django.contrib import messages

from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, FAQ
from order.models import ShopCart
from product.models import Product, Category, Images, Comment


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)#settingdeki bütün objeleri al
    sliderdata = Product.objects.filter(status=True)[:4]
    category = Category.objects.all()
    dayproducts = Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproducts = Product.objects.all().order_by('?')[:8]#? ürünlerin rastgele gelmesini sağlar
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()


    context = {'setting': setting,
               'category':category,
               'page':'home',
               'sliderdata':sliderdata,
               'dayproducts':dayproducts,
               'lastproducts':lastproducts,
               'randomproducts':randomproducts
               }
    return render(request, 'index.html', context)

def hakkimizda(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)#settingdeki bütün objeleri al
    context = {'setting': setting,
               'page':'hakkimizda',
               'category': category,
               }
    return render(request, 'hakkimizda.html', context)

def referanslarimiz(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)#settingdeki bütün objeleri al
    context = {'setting': setting, 'page':'referanslarimiz','category': category,}
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):
    if request.method == 'POST':#Form post edildiyse
        form= ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()#model ile bağlantı kur
            data.name = form.cleaned_data['name'] #formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()#veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir.")
            return  HttpResponseRedirect('/iletisim')

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)#settingdeki bütün objeleri al
    form = ContactFormu()
    context = {'setting': setting, 'form': form,'category': category,}
    return render(request, 'iletisim.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products': products,
               'category': category,
               'categorydata': categorydata
               }
    return render(request, 'products.html', context)

def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    context = {'category': category,
               'product': product,
               'images': images,
               'comments': comments
               }
    return render(request, 'product_detail.html',context)


def content_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.filter(category_id=id)
    link = '/product/'+str(product[0].id)+'/'+product[0].slug
    #return HttpResponse(link)
    return HttpResponseRedirect(link)#categoryidsi idye eşit olan ürünün likini gönderdik




def product_search(request):
    if request.method == 'POST':#Form post edildiyse
        form= SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query'] #formdan bilgiyi al
            cat_id = form.cleaned_data['cat_id']
            if cat_id == 0:
                products = Product.objects.filter(title__icontains=query)  # contains sorguyu içeren başlıkları bulur,i paremetresi büyük küçük harf duyarlılığı için
            else:
                products = Product.objects.filter(title__icontains=query,category_id=cat_id)
            context = {'products': products,
                       'category': category,
                       }
            return render(request,'products_search.html',context)

    return HttpResponseRedirect('/')

def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':#Form post edildiyse
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası ! Kullanıcı adı ya da şifre yanlış")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':  # Form post edildiyse
        form = SignUpForm(request.POST)
        if form.is_valid():#formun şartlarına bakılıyor,şifreler uyuyor mu vb
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request,"Üyeliğininz Tamamlandı..")
            return HttpResponseRedirect('/')


    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
                }
    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('number')#numbera göre sıralar
    context = {'category': category,
               'faq': faq,
               }
    return render(request, 'faq.html', context)