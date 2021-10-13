from django.urls import path

from . import views as uviews  # 2 tane views olduğundan sadece isim verdim
from user import views

urlpatterns = [

    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('orders/', views.orders, name='orders'),
    path('orderdetail/<int:id>', views.orderdetail, name='orderdetail'),
    path('newproduct/', views.user_newproduct, name='user_newproduct'),
    path('deleteuserproduct/<int:id>', views.deleteuserproduct, name='deleteuserproduct'),
    path('edituserproduct/<int:id>', views.edituserproduct, name='edituserproduct'),
    path('comments/', views.comments, name='comments'),
    path('products/', views.products, name='products'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('productaddimage/<int:id>', views.productaddimage, name='productaddimage'),

    # path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),#verileri alır,product_detail sayfasına gönderir
    # path('addcomment/<int:id>/', pviews.addcomment, name='addcomment'),#form kontrolü

]
