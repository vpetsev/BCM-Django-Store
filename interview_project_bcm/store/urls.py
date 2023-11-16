from django.urls import path
from . import views
from .views import category_list, product_list, purchase_report, new_purchase


app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),  # The root URL for the store app
    path('categories/', category_list, name='category_list'),
    path('categories/<int:category_id>/', product_list, name='product_list'),
    path('report/', purchase_report, name='purchase_report'),
    path('new-purchase/', new_purchase, name='new_purchase'),
    path('register/', views.register, name='register'),
]