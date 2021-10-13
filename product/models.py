from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (#açılan kutu
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(blank=True, max_length=100)
    keywords = models.CharField(blank=True, max_length=200)
    description = models.CharField(blank=True, max_length=200)

    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)

    slug = models.SlugField(null=False,unique=True)#metinsel çağırım için metin değişkeni
    parent = TreeForeignKey('self',blank=True, null=True, related_name='children', on_delete=models.CASCADE)#on_delete=models.CASCADE silme işleminde ona ait alt sınıfın silinmesini sağlar
    create_at = models.DateTimeField(auto_now_add=True)#sadece ekleme zamnında tarih için
    update_at = models.DateTimeField(auto_now=True)#her zaman tarih eklmesi için, hem güncelleme hem ekleme

    class MPTTMeta:
        order_insertion_by = ['title']


    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})

class Product(models.Model):
    STATUS = (#açılan kutu
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)#relation with Category table
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)  # relation with User table
    title = models.CharField(blank=True, max_length=150)
    keywords = models.CharField(blank=True, max_length=200)
    description = models.CharField(blank=True, max_length=200)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False,unique=True)  # metinsel çağırım için metin değişkeni
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now_add=True)  # sadece ekleme zamnında tarih için
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self): #alt kategori olduğu sürece artarda getitir
        return self.title  # titleyi döndürecek

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'slug':self.slug})


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)#on_delete product silindiğinde imagesların silinmesi için
    title = models.CharField(max_length=70, blank=True)#blank= true boş geçilebilmesi için
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title  # titleyi döndürecek
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class ProductImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title','image',]


class Comment(models.Model):
    STATUS = (#açılan kutu
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)#relation with Product table
    user = models.ForeignKey(User, on_delete=models.CASCADE)#relation with User table
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)  # sadece ekleme zamnında tarih için
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['rate', 'subject', 'comment']




