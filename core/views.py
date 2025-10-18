from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    return render(request, 'core/home.html', {'products': products})

def catalog(request):
    cat = request.GET.get('cat')
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    categories = Category.objects.all()
    if cat:
        category = get_object_or_404(Category, slug=cat)
        products = products.filter(category=category)
    return render(request, 'core/catalog.html', {'products': products, 'categories': categories})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'core/product_detail.html', {'product': product})