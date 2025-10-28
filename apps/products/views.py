from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,ProductGroup
from django.db.models.aggregates import Count
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
# ------------------------------------------------------------------------------------------------------------------------------------------------
# Special products
def special_products_list_view(request):
    special_products = Product.objects.filter(is_active=True,score__gt=4.5).order_by('-register_date')[:10]
    product_groups = ProductGroup.objects.filter(is_active=True,parent_group=None)[:3]
    return render(request,'products/partials/_special_products.html',{'special_products':special_products,'product_groups':product_groups})
# ------------------------------------------------------------------------------------------------------------------------------------------------
# New products
def new_products_list_view(request):
    special_products = Product.objects.filter(is_active=True).order_by('-register_date')[:5]
    product_groups = ProductGroup.objects.filter(is_active=True,parent_group=None)[:3]
    return render(request,'products/partials/_new_products.html',{'special_products':special_products,'product_groups':product_groups})
# ------------------------------------------------------------------------------------------------------------------------------------------------
# Popular categories
class PopularCategoriesListView(ListView):
    model = ProductGroup
    template_name = 'products/partials/_popular_categories.html'
    context_object_name = 'popular_categories'

    def get_queryset(self):
        query_set = ProductGroup.objects.filter(is_active=True).annotate(count=Count('product_groups')).order_by('-count')
        return query_set
# ------------------------------------------------------------------------------------------------------------------------------------------------
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product' 
# ------------------------------------------------------------------------------------------------------------------------------------------------
def related_products_view(request,slug):
    product = get_object_or_404(Product,slug=slug)
    related_products = []
    for group in product.product_groups.all() :
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_groups=group) & ~Q(id=product.id)))
    return render(request,'products/partials/_related_products.html',{'related_products':related_products[:5],})
# ------------------------------------------------------------------------------------------------------------------------------------------------
class ProductGropsListView(ListView):
    model = ProductGroup
    template_name = 'products/product_grops.html'
    context_object_name = 'product__groups'

    def get_queryset(self):
        query_set = ProductGroup.objects.filter(is_active=True).annotate(count=Count('product_groups')).order_by('-count')
        return query_set
    
# ------------------------------------------------------------------------------------------------------------------------------------------------
# List of products of each group

class ProductByGroupListView(ListView):
    model = Product
    template_name = 'products/products_by_group.html'
    context_object_name = 'products' 

    def get_queryset(self):
        self.group = get_object_or_404(ProductGroup,slug=self.kwargs['slug'])
        query_set = Product.objects.filter(is_active=True,product_groups=self.group)
        return query_set[:4]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.group
        return context
    
# ------------------------------------------------------------------------------------------------------------------------------------------------
# Product group list for filter
def get_product_groups(request):

    product_groups = ProductGroup.objects.annotate(count=Count('product_groups'))\
    .filter(Q(is_active=True) & ~Q(count=0))\
    .order_by('-count')

    return render(request,'products/partials/_product_groups.html',{'product_groups':product_groups})
# ------------------------------------------------------------------------------------------------------------------------------------------------
