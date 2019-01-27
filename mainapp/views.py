from django.shortcuts import render,  get_object_or_404
from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def get_basket(user):
    if user.is_authenticated:
        return user.basket_set.all().order_by('product__category')
    return []

def index(request):
    context = {

        'page_title': 'Главная',
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', context)

def contacts(request):

    contacts = [

        {'city': 'Москва',
         'phone': '+74959056178',},

        {'city': 'Санкт-Петербург',
         'phone': '+73899056178', },

        {'city': 'Краснодар',
         'phone': '+75559056178', }

    ]

    context = {

        'page_title': 'Контакты',
        'contacts': contacts,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/contacts.html', context)

def catalog(request, pk=None, page=1):
    categories = ProductCategory.objects.all()

    if pk:
        if pk == '0':
            catalog = Product.objects.all()
        else:
            catalog = Product.objects.filter(category__pk=pk)

        products_paginator = Paginator(catalog, 2)
        try:
            catalog = products_paginator.get_page(page)
        except PageNotAnInteger:
            catalog = products_paginator.get_page(1)
        except EmptyPage:
            catalog = products_paginator.get_page(products_paginator.num_pages)

        context = {

        'page_title': 'Каталог',
        'catalog': catalog,
        'categories': categories,
        'basket': get_basket(request.user),
        'category_pk': pk,

        }
        return render(request, 'mainapp/product_list.html',  context)

    else:
        context = {
            'title': 'каталог',
            'categories': categories,
            'basket': get_basket(request.user),
        }
    return render(request, 'mainapp/catalog.html', context)



def conference(request):

    context = {

        'page_title': 'Kонференция',
        'basket': get_basket(request.user),

    }
    return render(request, 'mainapp/conference.html', context)

def product(request, pk):
    categories = ProductCategory.objects.all()

    context = {
        'title': 'продукты',
        'categories': categories,
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/product.html', context)




