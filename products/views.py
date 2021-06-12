from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    current_category = None

    if request.GET:

        if 'category' in request.GET:
            category = request.GET['category']
            products = products.filter(category__name=category)
            current_category = Category.objects.filter(name=category)

        if 'search' in request.GET:
            query = request.GET['search']
            if not query:
                messages.error(
                    request, "Please enter a search criteria")
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query) | Q(
                description__icontains=query)| Q(
                category__name__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_category': current_category,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)