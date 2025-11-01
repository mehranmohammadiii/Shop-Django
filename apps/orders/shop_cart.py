from apps.products.models import Product

class ShopCart:
    def __init__(self,request):
        self.session = request.session
        self.shop_cart = self.session.setdefault('shop_cart', {})
        self.count = len(self.shop_cart.keys())
    # ----------------------    
    def add_to_shop_cart(self,product,count):
        product_id= str(product.id)
        if product_id not in self.shop_cart:
            self.shop_cart[product_id] = {"count":0,"price":product.price}  # 1 { "24" : { "count":0 ,"price" : 14000} }  #{ "45" : { "count":0 ,"price" : 52000} }
        self.shop_cart[product_id]["count"]+=int(count)                     # 2  { "54" : { "count":1 ,"price" : 14000} }  #{ "54" : { "count":1 ,"price" : 14000} }
        self.count = len(self.shop_cart.keys())
        self.save()
    # ----------------------    
    def save(self):
        self.session['shop_cart'] = self.shop_cart
        self.session.modified = True
    # ----------------------    
    def delete_from_shop_cart(self,product):
        product_id= str(product.id)
        del self.shop_cart[product_id]
        self.session.modified = True
    # ----------------------    
    def __iter__(self):
        list_id = self.shop_cart.keys()
        products = Product.objects.filter(id__in=list_id)
        temp = self.shop_cart.copy()

        for product in products:
            temp[str(product.id)]["product"]=product    #temp = { {'24' : product :{namr:'',price:'',slug:''} } }

        for item in temp.values():
            item["total_price"] = item['price']*item["count"]
            yield item

    def calc_total_price(self):
        sum=0
        for item in self.shop_cart.values():
            sum+=int(item['price'])*int(item['count'])
        return sum
    
    def update_count(self,product_id,count):
        product_id = str(product_id)
        if product_id in self.shop_cart :
            if count > 0 :
                self.shop_cart[product_id]['count'] = count
            else :
                del self.shop_cart['product_id']
            self.save()

#     def update_count(self, product_id, count):
#         """
#         تعداد یک محصول خاص را در سبد خرید آپدیت می‌کند.
#         اگر تعداد صفر باشد، محصول را حذف می‌کند.
#         """
#         product_id = str(product_id)
#         if product_id in self.shop_cart:
#             if count > 0:
#                 self.shop_cart[product_id]['count'] = count
#             else:
#                 # اگر کاربر تعداد را صفر وارد کرد، محصول را حذف کن
#                 del self.shop_cart[product_id]
            
#             self.save() # فراموش نکنیم که session 
# # ------------------------------------------------------------------------------------------------------------------------------
