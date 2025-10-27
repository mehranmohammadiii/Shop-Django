from django.shortcuts import render
from django.views.generic import ListView
from .models import Product,ProductGroup




# Special products
def special_products_list_view(request):
    special_products = Product.objects.filter(is_active=True,score__gt=4.5).order_by('-register_date')[:10]
    product_groups = ProductGroup.objects.filter(is_active=True,parent_group=None)[:3]
    return render(request,'products/partials/_special_products.html',{'special_products':special_products,'product_groups':product_groups})



# New products
def new_products_list_view(request):
    special_products = Product.objects.filter(is_active=True).order_by('-register_date')[:5]
    product_groups = ProductGroup.objects.filter(is_active=True,parent_group=None)[:3]
    return render(request,'products/partials/_new_products.html',{'special_products':special_products,'product_groups':product_groups})


# class NewProductsListView(ListView):
#     model = Product
#     template_name = 'products/partials/_special_products.html'
#     context_object_name = 'special_products'

#     def get_queryset(self):
#         query_set = Product.objects.filter(is_active=True).order_by('-register_date')[:5]
#         return query_set
    
# class ProductGroupsMenuView(ListView):

#     model = ProductGroup
#     template_name = 'products/partials/_product_groups_menu.html'
#     context_object_name = 'groups'

#     def get_queryset(self):
#         return ProductGroup.objects.filter(is_active=True, parent_group=None)