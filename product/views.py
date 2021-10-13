from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from product.models import CommentForm, Comment


def index(request):
    return HttpResponse("Product Page")


@login_required(login_url='/login')  # kişi login değilse işleme izin vermez
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')  # mesaj gittikten sonra olduğumuz yere dönmek için
    if request.method == 'POST':  # form post edildiyse
        form = CommentForm(request.POST)
        if form.is_valid():  # form geldi mi gelmedi mi kontrol eder
            current_user = request.user  # login olan userı getirir

            data = Comment()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.rate = form.cleaned_data['rate']
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')  # client computer ip adress
            data.save()  # veritabanını kaydet

            messages.success(request, "Yorumunuz başarı ile gönderilmiştir.Teşekkür ederiz")
            return HttpResponseRedirect(url)
    messages.error(request, "Yorumunuz kaydedilmedi.Lütfen kontrol ediniz!")
    return HttpResponseRedirect(url)
