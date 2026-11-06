from django.http import HttpResponse
from .models import ProductCategory, Product, Purchase
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import PurchaseForm, CustomUserCreationForm, PurchaseReportFilterForm

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
    category = get_object_or_404(ProductCategory, id=category_id)
    return render(request, 'store/product_list.html', {'products': products, 'category': category})


def purchase_report(request):
    purchases = Purchase.objects.all()
    categories = ProductCategory.objects.all()

    filter_form = PurchaseReportFilterForm(request.GET)
    valid_filters = filter_form.is_valid()
    if valid_filters:
        start_date = filter_form.cleaned_data['start_date']
        end_date = filter_form.cleaned_data['end_date']
        category = filter_form.cleaned_data['category_id']
        if start_date:
            purchases = purchases.filter(purchase_date__date__gte=start_date)
        if end_date:
            purchases = purchases.filter(purchase_date__date__lte=end_date)
        if category:
            purchases = purchases.filter(product__category=category)
    else:
        purchases = purchases.none()

    total_revenue = sum(purchase.product.price * purchase.quantity for purchase in purchases)

    return render(request, 'store/purchase_report.html', {
            'purchases': purchases,
            'categories': categories,
            'total_revenue': total_revenue,
            'filter_form': filter_form,
    }, status=200 if valid_filters else 400)

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
