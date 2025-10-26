from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product

def product_list(request, category_slug=None):
    categoties = Category.objects.all()
    products = Product.objects.filter(available=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    sort = request.GET.get('sort', '')
    if sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('name')

    return render(request, 'main/product/list.html',
                  {
                      'category': category,
                      'categories': categoties,
                      'products': products

                  })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    cart_product_form = CartAddProductForm()
    return render(request, 'main/product/detail.html', {'product': product,
                                                        'related_products': related_products,
                                                        'cart_product_form': cart_product_form})