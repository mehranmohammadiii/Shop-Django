from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,ProductGroup,Brand,Feature
from django.db.models.aggregates import Count
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from django.views import View
from .filters import ProductFilter
from django.core.paginator import Paginator
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
class ProductByGroupView(View):

    def get(self,request,*args,**kwargs):

        group = get_object_or_404(ProductGroup,slug=self.kwargs['slug'])
        products = Product.objects.filter(is_active=True,product_groups=group)

        # price filter
        filter_1 = ProductFilter(request.GET,queryset=products)
        products = filter_1.qs

        # brand filter
        brands_filter = request.GET.getlist('brand')  # 12 ,8 , 4
        if brands_filter :
            products = products.filter(product_brand__id__in=brands_filter)

        # feature filter
        features_filter = request.GET.getlist('feature')  
        if features_filter :
            products = products.filter(productfeatures__filter_value__id__in=features_filter).distinct()

        sort_type = request.GET.get('sort_type','0')
        if sort_type =='1' :
            products=products.order_by('price')
        elif sort_type =='2' :
            products=products.order_by('-price')

        group_slug = self.kwargs['slug']
        product_per_page = 4
        paginator = Paginator(products,product_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_count = products.count()

        context = {
            # 'products':products,
            'group':group,
            'group_slug':group_slug,
            'page_obj':page_obj,
            'product_count':product_count,
            'sort_type':sort_type,
        }
        return render(request,'products/products_by_group.html',context)






# ------------------------------------------------------------------------------------------------------------------------------------------------
# Product group list for filter
def get_product_groups(request):

    product_groups = ProductGroup.objects.annotate(count=Count('product_groups'))\
    .filter(Q(is_active=True) & ~Q(count=0))\
    .order_by('-count')

    return render(request,'products/partials/_product_groups.html',{'product_groups':product_groups})
# ------------------------------------------------------------------------------------------------------------------------------------------------
# List of brands for filters
def get_brand(request,slug):

    product__group = get_object_or_404(ProductGroup,slug=slug)

    brand_list_id=product__group.product_groups.filter(is_active=True).values('product_brand_id')
    brands = Brand.objects.filter(pk__in=brand_list_id)\
    .annotate(count=Count('product_brand'))\
    .filter(~Q(count=0))\
    .order_by('-count')

    # Brand.objects.filter(
    #     product_brand__product_groups=product__group,
    #     product_brand___is_active=True
    # ).annotate(
    # product_count=Count('product_brand', filter=Q(product_brand__product_groups=product_group)))/
    # .order_by('-product_count')


    return render(request,'products/partials/_brands.html',{'brands':brands})
# ------------------------------------------------------------------------------------------------------------------------------------------------
# Other lists of filters based on the values ​​of the attributes of the products within the group
def get_feature_for_filter(request,*args,**kwargs):

    product__group = get_object_or_404(ProductGroup,slug=kwargs['slug'])
    feature_list = product__group.productgroup_feature.all()

    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature]=feature.feature_value.all()
    
    return render(request,'products/partials/_feature_filter.html',{'feature_dict':feature_dict})
