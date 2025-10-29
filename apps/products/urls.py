from django.urls import path,include
from . import views
app_name = 'products'
urlpatterns = [
    path('special_products/',views.special_products_list_view,name='special_products'),
    path('new_products/',views.new_products_list_view,name='new_products'),
    path('popular_categories/',views.PopularCategoriesListView.as_view(),name='popular_categories'),
    path('related_product/<str:slug>/',views.related_products_view,name='related_product'),
    path('product_grops/',views.ProductGropsListView.as_view(),name='product_grops'),
    # path('group/<str:slug>/',views.ProductByGroupListView.as_view(),name='products_by_group'),
    path('group/<str:slug>/',views.ProductByGroupView.as_view(),name='products_by_group'),

    path('product_group_filter/',views.get_product_groups,name='product_group_filter'),
    path('brands/<str:slug>/',views.get_brand,name='brands'),
    path('feature_for_filter/<str:slug>/',views.get_feature_for_filter,name='feature_for_filter'),
    path('<str:slug>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('ckeditor/', include('ckeditor_uploader.urls')),


]



