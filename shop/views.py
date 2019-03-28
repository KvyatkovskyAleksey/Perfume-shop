from django.shortcuts import render, get_object_or_404
from .models import Category, Product, CarouselImages, Notes
from django.db.models import Q
import re
from cart.forms import CartAddProductForm

def index(request):
    first_carousel_image = CarouselImages.objects.all()[0]
    carousel_images = CarouselImages.objects.all()[1:]
    products = Product.objects.filter(available=True).order_by('-created')[:3]
    return render(request,
                  'shop/index.html',
                  {'first_carousel_image': first_carousel_image,
                   'carousel_images': carousel_images,
                   'products': products,
                   })

def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'products': products,
                   })

def product_list_by_note(request, note_slug):
    note = get_object_or_404(Notes, slug=note_slug)
    print(note)
    products = Product.objects.filter(heart_level=note).all()
    print(products)
    return render(request,
                'shop/product/list.html',
                {'note': note,
                 'products': products,
                 })

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
# Create your views here.
