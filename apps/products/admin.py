from django.contrib import admin
from .models import Brand,ProductGroup,Product,ProductFeature,Feature,ProductGallery,FeatureValue
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
class ProductFeatureInstansInlineAdmin(admin.TabularInline):
    model = ProductFeature
    extra=4

    class Media:
        css = {
            'all' : ('css/admin_style.css',)
        }

        js = ('','')
class ProductGalleryInstansInlineAdmin(admin.TabularInline):
    model = ProductGallery
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','previous_price','discount_percent','score','product_brand',)
    list_filter = ('price','discount_percent')
    search_fields = ('name',)
    ordering = ('price','name')
    inlines = [ProductFeatureInstansInlineAdmin,ProductGalleryInstansInlineAdmin]

# ----------------------------------------------------------------------------
@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('product','feature','value',)
    list_filter = ('product','value')
    search_fields = ('value',)
    ordering = ('product',)
# ----------------------------------------------------------------------------
class FeatureValueInstansInlineAdmin(admin.TabularInline):
    model = FeatureValue
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name','display_groups','display_feature_value')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [FeatureValueInstansInlineAdmin]

    # def formfield_for_manytomany(self,db_field):
    #     if db_field == =

    def display_groups(self,obj):
        return ', '.join([group.name for group in obj.productgroup_feature.all()])
    
    def display_feature_value(self,obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_value.all()])
    
    display_groups.short_description='گروه های دارای این ویژگی'
    display_feature_value.short_description='مقادیر ممکن برای این ویژگی'

