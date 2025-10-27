from django.contrib import admin
from .models import Brand,ProductGroup,Product
from django.db.models.aggregates import Count
# ----------------------------------------------------------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
# ----------------------------------------------------------------------------
class ProductGroupInstansInlineAdmin(admin.TabularInline):
    model = ProductGroup
# ----------------------------------------------------------------------------
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('name','parent_group','is_active','slug')
    list_filter = ('name','parent_group')
    search_fields = ('name',)
    ordering = ('name','parent_group')
    inlines = [ProductGroupInstansInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs.annotate(sub_group = Count('parent_group'))
        return qs
    
    # def count_sub_group(self,obj):
    #     return obj.sub_group
    
    # count_sub_group.short_description='تعداد زیر گروه ها'
# ----------------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','previous_price','discount_percent','score','product_brand',)
    list_filter = ('price','discount_percent')
    search_fields = ('price',)
    ordering = ('price','name')
# ----------------------------------------------------------------------------
