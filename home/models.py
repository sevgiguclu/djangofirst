from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import TextInput, ModelForm, Textarea
from django.utils.safestring import mark_safe


class Setting(models.Model):
    STATUS = (  # açılan kutu
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    address = models.CharField(blank=True, max_length=150)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    smtpserver = models.CharField(blank=True, max_length=20)
    smtpemail = models.CharField(blank=True, max_length=20)
    smtppasword = models.CharField(blank=True, max_length=20)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)  # sadece ekleme zamnında tarih için
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title  # titleyi döndürecek

class ContactFormMessage(models.Model):
    STATUS = (
            ('New', 'New'),
            ('Read', 'Read'),
            ('Closed', 'Closed')
    )

    name = models.CharField(blank=True, max_length=30)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.CharField(max_length=250)
    status = models.CharField(choices=STATUS, max_length=10, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactFormu(ModelForm):
    class Meta:
        model = ContactFormMessage#hangi modele ait
        fields = ['name', 'email', 'subject', 'message']#formda görülecek elemanlar
        widgets = {#ayrıntı ayarları,  içinde yazacaklar
            'name' : TextInput(attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'subject' : TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'email' : TextInput(attrs={'class': 'input', 'placeholder': 'Email Adress'}),
            'message' : Textarea(attrs={'class': 'input', 'placeholder': 'Your Message', 'rows': '5'}),
        }


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return  self.user.first_name + ' ' + self.user.last_name + ' ' + '[' + self.user.username + ']'


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile#hangi modele ait
        fields = ['phone', 'address', 'city', 'image']


class FAQ(models.Model):
    STATUS = (  # açılan kutu
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    number = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = models.TextField()#sınır koymazsan sınır olmaz
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)  # sadece ekleme zamnında tarih için
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question  # questionı döndürecek

