from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_POST
import json
# ----------------------------------------------------------------------------------------------------------------
class ShopCartView(View):
    def get (self , request):
        shop_cart = ShopCart(request)
        return render(request,"orders/shop_cart.html",{"shop_cart":shop_cart})
# ----------------------------------------------------------------------------------------------------------------
def add_to_shop_cart(request):
    product_id = request.POST.get('product_id')
    count = request.POST.get('count')

    shop_cart = ShopCart(request)
    product=get_object_or_404(Product,id=product_id)
    shop_cart.add_to_shop_cart(product,count)
    # return HttpResponse(shop_cart.count)
    # return HttpResponse(shop_cart.__len__())
    return JsonResponse({'status': 'success', 'message': 'محصول به سبد اضافه شد'})

# ----------------------------------------------------------------------------------------------------------------------------
def show_shop_cart(request):
    shop_cart = ShopCart(request)
    # total_price=shop_cart.calc_total_price()
    total_price=shop_cart.get_total_price()

    delivery= 25000
    tax = 0.09*total_price
    order_final_price =total_price+delivery+tax
    if total_price > 500000:
        delivery=0
    
    context ={"shop_cart":shop_cart,
            #   "shop_cart_count":shop_cart.count,
                "shop_cart_count":shop_cart.__len__(),

              'total_price':total_price,
              'delivery':delivery,
              'tax':tax,
              'order_final_price':order_final_price
              }
    return render(request,"orders/partials/_show_shop_cart.html",context)

# ----------------------------------------------------------------------------------------------------------------------------
@require_POST
def delete_from_shop_cart(request):
    product_id = request.POST.get('product_id')

    shop_cart = ShopCart(request)
    product=get_object_or_404(Product,id=product_id)
    shop_cart.delete_from_shop_cart(product)
    # return redirect("orders:show_shop_cart")
    return show_shop_cart(request)
# ----------------------------------------------------------------------------------------------------------------------------
# @require_POST 
# def update_shop_cart(request):
#     try:
#         data = json.loads(request.body)
#         updated_items = data.get('items')

#         if updated_items is None:
#             return JsonResponse({'status': 'error', 'message': 'اطلاعات نامعتبر است.'}, status=400)

#         shop_cart = ShopCart(request)

#         for item in updated_items:
#             product_id = item.get('product_id')
#             count = int(item.get('count', 0)) 

#             shop_cart.update_count(product_id, count)
        
#         return JsonResponse({'status': 'success', 'message': 'سبد خرید با موفقیت به‌روزرسانی شد.'})

#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
# ----------------------------------------------------------------------------------------------------------------------------
@require_POST
def update_shop_cart(request):
    try:
        data = json.loads(request.body)
        updated_items = data.get('items')

        if updated_items is None:
            return HttpResponse("اطلاعات نامعتبر است.", status=400)

        shop_cart = ShopCart(request)

        for item in updated_items:
            product_id = item.get('product_id')
            count = int(item.get('count', 0))
            shop_cart.update_count(product_id, count)
        
        # return render(request, 'orders/partials/_show_shop_cart.html', {"shop_cart": shop_cart})
        # return redirect("orders:show_shop_cart")
        return show_shop_cart(request)

    except Exception as e:
        return HttpResponse(f"خطایی در سرور رخ داد: {e}", status=500)
# ----------------------------------------------------------------------------------------------------------------------------
def status_of_shop_cart(request):
    shop_cart = ShopCart(request)
    # return JsonResponse({'count': shop_cart.count})
    return JsonResponse({'count': shop_cart.__len__()})

# ----------------------------------------------------------------------------------------------------------------------------
