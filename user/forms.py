from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import Select, TextInput, EmailInput, FileInput, Textarea

from home.models import UserProfile
from product.models import Product


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'username'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last_name'}),
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'address'}),
            'city': Select(attrs={'class': 'input', 'placeholder': 'city'}, choices=CITY),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            # dosya upload edebilmek için FileInput
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'keywords', 'description', 'image', 'price', 'amount', 'slug', 'detail', ]
        widgets = {
            'category': Select(attrs={'class': 'input', }),
            'title': TextInput(attrs={'class': 'input', }),
            'keywords': TextInput(attrs={'class': 'input', }),
            'description': TextInput(attrs={'class': 'input', }),
            'price': TextInput(attrs={'class': 'input', }),
            'amount': TextInput(attrs={'class': 'input', }),
            'detail': CKEditorWidget(),
            'image': FileInput(attrs={'class': 'input', }),
            'slug': TextInput(attrs={'class': 'input', }),
            # dosya upload edebilmek için FileInput
        }
