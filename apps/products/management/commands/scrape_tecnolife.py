# import requests
# from bs4 import BeautifulSoup
# from django.core.management.base import BaseCommand
# import re
# from apps.products.models import Product,Brand,ProductGroup
# # ---------------------------------------------------------------------------------------------------
# def clean_price(price_string):
#     if not price_string: return 0
#     try:
#         cleaned_string = re.sub(r'[^\d]', '', price_string)
#         return int(cleaned_string) if cleaned_string else 0
#     except (ValueError, TypeError):
#         return 0
    

# class Command(BaseCommand):
#     help = 'Scrap and display product names from specified categories in Technolife'

#     def handle(self, *args, **options):

#         categories_to_scrape = {
#             'موبایل': 'https://www.technolife.com/product/list/69_800/تمام-گوشی‌های-موبایل',
#             'لپ تاپ و تبلت': 'https://www.technolife.com/product/list/164_163_130/تمامی-کامپیوترها-و-لپ-تاپ-ها',
#             'ساعت و بند هوشمند': 'https://www.technolife.com/product/list/30/ساعت-و-بند-هوشمند',
#         }

#         self.stdout.write(self.style.SUCCESS('>>> The product scrapping operation has begun...'))

#         new_products_count = 0

#         for group_name, url in categories_to_scrape.items():
            
#             main_group = ProductGroup.objects.get(name=group_name, parent_group=None)
#             self.stdout.write(self.style.WARNING(f'\n====================\nCategory: {group_name}\n===================='))
#             self.stdout.write(f'>>> Sending request to: {url}')
            
#             try:
#                 response = requests.get(url, timeout=10)
#                 response.raise_for_status() 
#             except requests.exceptions.RequestException as e:
#                 self.stdout.write(self.style.ERROR(f'!!! An error occurred while retrieving the category page: {e}'))
#                 continue 

#             soup = BeautifulSoup(response.content, "html.parser")
            
#             product_containers = soup.select("section.relative.w-full")
            
#             if not product_containers:
#                 self.stdout.write(self.style.WARNING('>>> No products were found on this page.'))
#                 continue

#             self.stdout.write(self.style.SUCCESS(f'>>> {len(product_containers)} Product found on this page. Product names:'))
            
#             for item in product_containers:

#                 try:
                    
#                     try:
#                         product_name_tag = item.select_one("h2")
#                         product_name = product_name_tag.text.strip()
#                         self.stdout.write(f'  -> {product_name}\t{type(product_name)}')
#                     except :
#                         self.stdout.write(self.style.ERROR(f'Error getting product name: {e}'))
#                         product_name = None
#                     # --------------------
#                     try :
#                         score=item.select_one("p.text-sm").text
#                         self.stdout.write(f'  -> {score}\t{type(score)}')
#                     except :
#                         self.stdout.write(self.style.ERROR(f'  -> null'))
#                         score=None
#                     # --------------------                   
#                     try :
#                         discountpercent=item.select_one("span.flex").text
#                         self.stdout.write(f'  -> {discountpercent}\t{type(discountpercent)}')
#                     except :
#                         self.stdout.write(self.style.ERROR(f'  -> null'))
#                         discountpercent=None
#                     # --------------------                      
#                     try :
#                         previousprice=item.select_one("div.items-end div.flex p").text
#                         # previousprice=clean_price(previousprice)
#                         self.stdout.write(f'  -> {previousprice}\t{type(previousprice)}')
#                     except:
#                         self.stdout.write(self.style.ERROR(f'  -> null'))
#                         previousprice=None
#                     # --------------------
#                     try :
#                         Newprice=item.select_one("div.pt-6 div.flex p.leading-5").contents[0]
#                         # Newprice=clean_price(Newprice)
#                         self.stdout.write(f'  -> {Newprice}\t{type(Newprice)}')
#                     except:
#                         self.stdout.write(self.style.ERROR(f'  -> null'))
#                         Newprice=None
#                     # --------------------

#                     score_final = float(score) if score else 0.0
#                     discount_final = int(discountpercent) if discountpercent else 0
#                     previous_price_final = clean_price(previousprice)
#                     new_price_final = clean_price(Newprice)

#                     brand_name = "متفرقه" 
#                     if "شیائومی" in product_name: brand_name = "شیائومی"
#                     elif "اپل" in product_name or 'آیفون' in  product_name : brand_name = "اپل"
#                     elif "پوکو" in product_name: brand_name = "پوکو"
#                     elif "سامسونگ" in product_name: brand_name = "سامسونگ"
#                     elif "داریا" in product_name: brand_name = "داریا"
#                     elif "هانوفر" in product_name: brand_name = "هانوفر"
#                     elif "نوکیا" in product_name: brand_name = "نوکیا"
#                     elif "ایسوس" in product_name: brand_name = "ایسوس"
#                     elif "آنر" in product_name: brand_name = "آنر"
#                     elif "لنوو" in product_name: brand_name = "لنوو"
#                     elif "اچ پی" in product_name: brand_name = "اچ پی"
#                     elif "ایسر" in product_name: brand_name = "ایسر"

#                     brand, _ = Brand.objects.get_or_create(name=brand_name)


#                     product, created = Product.objects.get_or_create(
#                         name=product_name,
#                         defaults={
#                             'price': new_price_final,
#                             'previous_price': previous_price_final,
#                             'discount_percent': discount_final,
#                             'score': score_final,
#                             'product_brand': brand,
#                             'is_active': True,
#                         }
#                     )
                    
#                     product.product_groups.add(main_group)
                    
#                     if created:
#                         new_products_count += 1
#                         self.stdout.write(self.style.SUCCESS(f'  -> "{product_name}\t{new_products_count}" Added to the database.'))

#                     self.stdout.write(self.style.SUCCESS(f'  -> -----------------------------------------------------'))


#                 except Exception as e:
#                     self.stdout.write(self.style.ERROR(f'   !!! Error processing an item: {e}'))
#                     continue

#         self.stdout.write(self.style.SUCCESS('\n>>> The operation was completed successfully.'))

# ---------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
import re
from apps.products.models import Product,Brand,ProductGroup
# ---------------------------------------------------------------------------------------------------
def clean_price(price_string):
    if not price_string: return 0
    try:
        cleaned_string = re.sub(r'[^\d]', '', price_string)
        return int(cleaned_string) if cleaned_string else 0
    except (ValueError, TypeError):
        return 0
    

class Command(BaseCommand):
    help = 'Scrap and display product names from specified categories in Technolife'

    def handle(self, *args, **options):

        categories_to_scrape = {
            'موبایل': 'https://www.technolife.com/product/list/69_800/تمام-گوشی‌های-موبایل',
            'لپ تاپ و تبلت': 'https://www.technolife.com/product/list/164_163_130/تمامی-کامپیوترها-و-لپ-تاپ-ها',
            'ساعت و بند هوشمند': 'https://www.technolife.com/product/list/30/ساعت-و-بند-هوشمند',
        }

        self.stdout.write(self.style.SUCCESS('>>> The product scrapping operation has begun...'))

        new_products_count = 0

        for group_name, url in categories_to_scrape.items():
            
            main_group = ProductGroup.objects.get(name=group_name, parent_group=None)
            self.stdout.write(self.style.WARNING(f'\n====================\nCategory: {group_name}\n===================='))
            self.stdout.write(f'>>> Sending request to: {url}')
            
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status() 
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'!!! An error occurred while retrieving the category page: {e}'))
                continue 

            soup = BeautifulSoup(response.content, "html.parser")
            
            product_containers = soup.select("section.relative.w-full")
            
            if not product_containers:
                self.stdout.write(self.style.WARNING('>>> No products were found on this page.'))
                continue

            self.stdout.write(self.style.SUCCESS(f'>>> {len(product_containers)} Product found on this page. Product names:'))
            
            for item in product_containers:

                try:
                    
                    try:
                        product_name_tag = item.select_one("h2")
                        product_name = product_name_tag.text.strip()
                        self.stdout.write(f'  -> {product_name}\t{type(product_name)}')
                    except :
                        self.stdout.write(self.style.ERROR(f'Error getting product name: {e}'))
                        product_name = None
                    # --------------------
                    try :
                        score=item.select_one("p.text-sm").text
                        self.stdout.write(f'  -> {score}\t{type(score)}')
                    except :
                        self.stdout.write(self.style.ERROR(f'  -> null'))
                        score=None
                    # --------------------                   
                    try :
                        discountpercent=item.select_one("span.flex").text
                        self.stdout.write(f'  -> {discountpercent}\t{type(discountpercent)}')
                    except :
                        self.stdout.write(self.style.ERROR(f'  -> null'))
                        discountpercent=None
                    # --------------------                      
                    try :
                        previousprice=item.select_one("div.items-end div.flex p").text
                        # previousprice=clean_price(previousprice)
                        self.stdout.write(f'  -> {previousprice}\t{type(previousprice)}')
                    except:
                        self.stdout.write(self.style.ERROR(f'  -> null'))
                        previousprice=None
                    # --------------------
                    try :
                        Newprice=item.select_one("div.pt-6 div.flex p.leading-5").contents[0]
                        # Newprice=clean_price(Newprice)
                        self.stdout.write(f'  -> {Newprice}\t{type(Newprice)}')
                    except:
                        self.stdout.write(self.style.ERROR(f'  -> null'))
                        Newprice=None
                    # --------------------
                    try :
                        memory=item.select("div.h-12 p")[0].text
                        self.stdout.write(f'  -> {memory}\t{type(memory)}')
                    except :
                        self.stdout.write(self.style.ERROR(f'  -> null'))
                        memory=None
                    # --------------------
                    try :
                        selfiecamera=item.select("div.h-12 p")[1].text
                        self.stdout.write(f'  -> {selfiecamera}\t{type(selfiecamera)}')
                    except :
                        self.stdout.write(self.style.ERROR(f'  -> null'))
                        selfiecamera=None
                    # --------------------
                    try :
                        Rearcamera=item.select("div.h-12 p")[2].text
                        self.stdout.write(f'  -> {Rearcamera}\t{type(Rearcamera)}')
                    except :
                        self.stdout.write(self.style.ERROR(f'  -> null'))
                        Rearcamera=None
                    # --------------------
                    try :
                        Batterycapacity=item.select("div.h-12 p")[3].text
                        self.stdout.write(f'  -> {Batterycapacity}\t{type(Batterycapacity)}')
                    except :
                        self.stdout.write(self.style.ERROR(f'  -> null'))
                        Batterycapacity=None
                    # --------------------



                    # score_final = float(score) if score else 0.0
                    # discount_final = int(discountpercent) if discountpercent else 0
                    # previous_price_final = clean_price(previousprice)
                    # new_price_final = clean_price(Newprice)

                    # brand_name = "متفرقه" 
                    # if "شیائومی" in product_name: brand_name = "شیائومی"
                    # elif "اپل" in product_name or 'آیفون' in  product_name : brand_name = "اپل"
                    # elif "پوکو" in product_name: brand_name = "پوکو"
                    # elif "سامسونگ" in product_name: brand_name = "سامسونگ"
                    # elif "داریا" in product_name: brand_name = "داریا"
                    # elif "هانوفر" in product_name: brand_name = "هانوفر"
                    # elif "نوکیا" in product_name: brand_name = "نوکیا"
                    # elif "ایسوس" in product_name: brand_name = "ایسوس"
                    # elif "آنر" in product_name: brand_name = "آنر"
                    # elif "لنوو" in product_name: brand_name = "لنوو"
                    # elif "اچ پی" in product_name: brand_name = "اچ پی"
                    # elif "ایسر" in product_name: brand_name = "ایسر"

                    # brand, _ = Brand.objects.get_or_create(name=brand_name)


                    # product, created = Product.objects.get_or_create(
                    #     name=product_name,
                    #     defaults={
                    #         'price': new_price_final,
                    #         'previous_price': previous_price_final,
                    #         'discount_percent': discount_final,
                    #         'score': score_final,
                    #         'product_brand': brand,
                    #         'is_active': True,
                    #     }
                    # )
                    
                    # product.product_groups.add(main_group)
                    
                    # if created:
                    #     new_products_count += 1
                    #     self.stdout.write(self.style.SUCCESS(f'  -> "{product_name}\t{new_products_count}" Added to the database.'))

                    self.stdout.write(self.style.SUCCESS(f'  -> -----------------------------------------------------'))


                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'   !!! Error processing an item: {e}'))
                    continue

        self.stdout.write(self.style.SUCCESS('\n>>> The operation was completed successfully.'))

# ---------------------------------------------------------------------------------------------------
