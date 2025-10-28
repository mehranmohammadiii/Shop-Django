from django.core.management.base import BaseCommand
from apps.products.models import Product

class Command(BaseCommand):
    help = 'یک اسکریپت یک‌بار مصرف برای ساخت اسلاگ برای محصولات موجود که اسلاگ ندارند'

    def handle(self, *args, **options):
        products_without_slug = Product.objects.filter(slug__isnull=True)
        
        if not products_without_slug.exists():
            self.stdout.write(self.style.SUCCESS('>>> All products already have slugs.'))
            return

        self.stdout.write(self.style.WARNING(f'>>> {products_without_slug.count()} Product found without slug. Creating slug...'))

        updated_count = 0
        for product in products_without_slug:
            product.save()
            updated_count += 1
            self.stdout.write(f' -> Slug for the product"{product.name}" Made: {product.slug}')

        self.stdout.write(self.style.SUCCESS(f'\n>>>The operation was completed successfully. {updated_count} The product has been updated.'))