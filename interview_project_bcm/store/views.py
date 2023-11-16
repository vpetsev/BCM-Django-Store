from django.http import HttpResponse
from .models import ProductCategory, Product, Purchase
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import PurchaseForm, CustomUserCreationForm

import datetime

def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

# View for displaying all categories
def category_list(request):
    categories = ProductCategory.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


# View for displaying products in a specific category
def product_list(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    category = ProductCategory.objects.get(id=category_id)
    return render(request, 'store/product_list.html', {'products': products, 'category': category})


def purchase_report(request):
    purchases = Purchase.objects.all()
    categories = ProductCategory.objects.all()

    # Filter by datetime
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        purchases = purchases.filter(purchase_date__date__range=[start_date.date(), end_date.date()])

    # Filter by category
    category_id = request.GET.get('category_id')
    if category_id:
        purchases = purchases.filter(product__category__id=category_id)

    total_revenue = sum(purchase.product.price * purchase.quantity for purchase in purchases)

    return render(request, 'store/purchase_report.html', {
            'purchases': purchases,
            'categories': categories,
            'total_revenue': total_revenue,
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login or other page
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def new_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.save()
            return redirect(reverse('store:index'))  # Redirect to a relevant view
    else:
        form = PurchaseForm()
    return render(request, 'store/new_purchase.html', {'form': form})
