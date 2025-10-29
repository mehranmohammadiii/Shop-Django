from django.contrib import admin
from .models import Brand,ProductGroup,Product,ProductFeature,Feature,ProductGallery,FeatureValue
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description,order_field
# ---------------------------------------------------------------------------------------------------------------------------------------------
def de_active_group(modeladmin,request,queryset):   #Action
    res = queryset.update(is_active=False)
    message = f'تعداد {res} کالا با موفقیت غیر فعال شد'
    modeladmin.message_user(request,message)
    # ---------------------
def active_group(modeladmin,request,queryset):   #Action
    res = queryset.update(is_active=True)
    message = f'تعداد {res} کالا با موفقیت  فعال شد'
    modeladmin.message_user(request,message)
    # ---------------------
def export_json(modeladmin,request,queryset):
    response = HttpResponse(content_type='application/json')
    serializers.serialize('json',queryset,stream=response)
    return response
# --------------------------------------------------------------------------------------------------------------------------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
# ---------------------------------------------------------------------------------------------------------------------------------------------
class ProductGroupInstansInlineAdmin(admin.TabularInline):
    model = ProductGroup
# -----------------
class GroupFilter(SimpleListFilter):
    title = 'گروه محصولات'
    parameter_name = 'group'
    # -------------------
    def lookups(self, request, model_admin):
        sub_groups = ProductGroup.objects.filter(~Q(parent_group=None))
        groups = set([item.parent_group for item in sub_groups])
        return [(item.id, item.name) for item in groups]
    # -------------------
    def queryset(self, request, queryset):
        if self.value()!=None :
            return queryset.filter(Q(parent_group=self.value()))
        return queryset
# -----------------
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('name','parent_group','is_active','slug','count_sub_group','count_product_of_groups',)
    # list_filter = ('name',('parent_group',DropdownFilter),)
    list_filter = (GroupFilter,'is_active')
    search_fields = ('name',)
    ordering = ('name','parent_group')
    inlines = [ProductGroupInstansInlineAdmin]
    actions=[de_active_group,active_group,export_json]
    list_editable = ['is_active']

    # ---------------------
    # def get_queryset(self, request):
    #     qs = super(ProductGroupAdmin).get_queryset(request)
    #     qs.annotate(sub_group = Count('parent_group'))
    #     return qs
    
    def get_queryset(self, *args,**kwargs):
        qs =super(ProductGroupAdmin,self).get_queryset(*args,**kwargs)
        qs = qs.annotate(sub_group=Count('parent_group'))
        qs = qs.annotate(product_of_groups=Count('product_groups'))
        return qs
    # ---------------------
    def count_sub_group(self,obj):
        return obj.sub_group
    # ---------------------
    @short_description('تعداد کالاهای درون گروه')
    @order_field('product_groups')
    def count_product_of_groups(self,obj):
        return obj.product_of_groups
    # ---------------------
    count_sub_group.short_description='تعداد زیر گروه ها'
    de_active_group.short_description = 'غیر فعال کردن'
    active_group.short_description = ' فعال کردن'
    export_json.short_description = '  خروجی جیسونی'

# ------------------------------------------------------------------------------------------------------------------------------------
class ProductFeatureInstansInlineAdmin(admin.TabularInline):
    model = ProductFeature
    extra=4
    # ---------------------
    class Media:
        css = {
            'all' : ('css/admin_style.css',)
        }

        js = ('','')
# ---------------------
class ProductGalleryInstansInlineAdmin(admin.TabularInline):
    model = ProductGallery
# --------------------- 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','previous_price','discount_percent','score','product_brand','display_product_groups')
    list_filter = ('price','discount_percent')
    search_fields = ('name',)
    ordering = ('price','name')
    inlines = [ProductFeatureInstansInlineAdmin,ProductGalleryInstansInlineAdmin]
    actions =[de_active_group,active_group]
    # ---------------------
    def display_product_groups(self,obj):
        return ', '.join([group.name for group in obj.product_groups.all()])
    # ---------------------  
    # Hide main categories when adding new products
     
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == 'product_groups' :
    #         kwargs['queryset'] = ProductGroup.objects.filter(~Q(parent_group=None))
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)
    # ---------------------
    # Customize the admin panel layout
    # fieldsets = (
    #     ('اطلاعات محصول',{
    #         'fields': (
    #             'name',
    #             'slug',
    #             ('product_groups','product_brand','is_active'),
    #             'short_text',
    #          )}),

    # )
    
    display_product_groups.short_description = ' گروه های کالا'

# -------------------------------------------------------------------------------------------------------------------------------------------
@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('product','feature','value',)
    list_filter = ('product','value')
    search_fields = ('value',)
    ordering = ('product',)
# -----------------------------------------------------------------------------------------------------------------------------------------------
class FeatureValueInstansInlineAdmin(admin.TabularInline):
    model = FeatureValue
 # ---------------------
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name','display_groups','display_feature_value')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [FeatureValueInstansInlineAdmin]
    # ---------------------
    # def formfield_for_manytomany(self,db_field):
    #     if db_field == =

    def display_groups(self,obj):
        return ', '.join([group.name for group in obj.productgroup_feature.all()])
    # ---------------------   
    def display_feature_value(self,obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_value.all()])
    # ---------------------  
    display_groups.short_description='گروه های دارای این ویژگی'
    display_feature_value.short_description='مقادیر ممکن برای این ویژگی'

