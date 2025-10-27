from django.urls import path
from . import views
app_name = 'products'
urlpatterns = [
    path('special_products/',views.special_products_list_view,name='special_products'),
    path('new_products/',views.new_products_list_view,name='new_products')

]



