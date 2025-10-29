from django.db import models
from django.utils import timezone
from django.utils.text import slugify
# from ckeditor_uploader.fields import RichTextUploadingField
# ------------------------------------------------------------------------------------------------------
class Brand(models.Model):
    name = models.CharField(max_length=50,verbose_name='نام برند')
    image = models.ImageField(upload_to='images/product',verbose_name='تصویر')
    slug = models.SlugField(max_length=100,null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta :
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'
# ------------------------------------------------------------------------------------------------------
class ProductGroup(models.Model):
    name = models.CharField(max_length=50,verbose_name='نام گروه')
    # image = models.ImageField(upload_to='images/group',verbose_name='تصویر گروه')
    short_text = models.CharField(max_length=200,null=True,blank=True,verbose_name='متن توضیحات')
    is_active = models.BooleanField(default=False,verbose_name='وضعیت')
    slug = models.SlugField(max_length=100,null=True)
    parent_group = models.ForeignKey('ProductGroup',null=True,blank=True,on_delete=models.CASCADE,related_name='parent',verbose_name='والد گروه')

    def __str__(self):
        return f'{self.name}'
    
    class Meta :
        verbose_name = 'گروه'
        verbose_name_plural = 'گروه ها'
# ------------------------------------------------------------------------------------------------------
class Feature(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام ویژگی')
    productgroup_feature = models.ManyToManyField(ProductGroup,related_name='productgroup_feature',verbose_name='ویژگی گروه')

    def __str__(self):
        return f'{self.name}'
    
    class Meta :
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'
# ------------------------------------------------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=300,verbose_name='نام محصول')
    short_text = models.TextField(max_length=500,null=True,blank=True,verbose_name='متن خلاصه')
    # short_text = RichTextUploadingField(blank=True,verbose_name='متن خلاصه')
    text = models.TextField(null=True,blank=True,verbose_name='متن و توضیخات')
    slug = models.SlugField(max_length=250,null=True,blank=True,unique=True,allow_unicode=True)

    price = models.PositiveIntegerField(default=0,verbose_name='قیما نهایی')
    previous_price = models.PositiveIntegerField(default=0, verbose_name='قیمت قبل')
    discount_percent = models.PositiveIntegerField(default=0, verbose_name='درصد تخفیف')
    score = models.FloatField(default=0.0, verbose_name='امتیاز')

    
    # image = models.ImageField(upload_to='images/product',default='',null=True,blank=True,verbose_name='تصویر محصول')
    is_active = models.BooleanField(default=False,verbose_name='وضعیت')
    register_date = models.DateField(auto_now_add=True,verbose_name="تاریخ ثبت")
    publication_date =models.DateField(default=timezone.now,verbose_name="تاریخ انتشار")
    update_date =models.DateField(auto_now=True,verbose_name="تاریخ آخرین ویرایش")
    product_brand = models.ForeignKey(Brand,related_name='product_brand',null=True,on_delete=models.CASCADE,verbose_name='نام برند')
    product_groups = models.ManyToManyField(ProductGroup,related_name='product_groups',verbose_name='گروه های محصول')
    product_features = models.ManyToManyField(Feature,through='ProductFeature',verbose_name='ویژگی های محصول')
    def __str__(self):
        return f'{self.name}'
    
    def save(self,*args, **kwargs):
        if not self.slug :
            self.slug = slugify(self.name,allow_unicode=True)
        return super().save(*args, **kwargs)
    
    class Meta :
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
# ------------------------------------------------------------------------------------------------------
class FeatureValue(models.Model):
    value_title = models.CharField(max_length=100,verbose_name='عنوان مقدار')
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE,null=True,blank=True,related_name='feature_value',verbose_name='ویژگی')

    def __str__(self):
        return f'{self.id}\t{self.value_title}'
    class Meta :
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقدار ویژگی ها'
# ------------------------------------------------------------------------------------------------------
class ProductFeature(models.Model):
    product = models.ForeignKey(Product,related_name='productfeatures',on_delete=models.CASCADE,verbose_name='محصول')
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name='ویژگی')
    value = models.CharField(max_length=100,verbose_name='مقدار')
    filter_value = models.ForeignKey(FeatureValue,on_delete=models.CASCADE,null=True,blank=True,verbose_name='مقدار فیلتر ویژگی')
    def __str__(self):
        return f'{self.product}\t{self.feature}\t{self.value}'
    
    class Meta :
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی های محصولات'
# ------------------------------------------------------------------------------------------------------
class ProductGallery(models.Model):
    image = models.ImageField(upload_to='images/product/productgallery',verbose_name='تصویر محصول')
    product = models.ForeignKey(Product,related_name='product_images',on_delete=models.CASCADE,verbose_name="محصول")

    def __str__(self):
        return self.image
    
    class Meta :
        verbose_name = 'تصویر '
        verbose_name_plural = ' تصویر ها'
# ------------------------------------------------------------------------------------------------------
