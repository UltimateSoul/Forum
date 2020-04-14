from django.conf import settings
from django.db import models

from shop.helpers import get_product_path


class Product(models.Model):
    """Represents in-game or site product, that user can buy and use"""

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=get_product_path)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=7)

    def __repr__(self):
        return f'Product {self.name}  Price: {self.price}'


class ProductCheckout(models.Model):
    """Model that is used in statistics of bought products"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_profile = models.ForeignKey('UserShopProfile',
                                        on_delete=models.CASCADE,
                                        related_name='product_checkouts')
    created_at = models.DateField(auto_now_add=True)


class UserShopProfile(models.Model):
    """Serves user products"""

    customer_id = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

