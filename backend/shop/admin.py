from django.contrib import admin

from shop.models import Product, ProductCheckout, UserShopProfile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'preview')

    @staticmethod
    def preview(obj):
        return obj.description[:40]


@admin.register(ProductCheckout)
class ProductCheckoutAdmin(admin.ModelAdmin):

    list_display = ('product_name', 'profile', 'created_at')

    @staticmethod
    def product_name(obj):
        return obj.product.name

    @staticmethod
    def profile(obj):
        return f'Profile of {obj.product_profile.user.username}'


@admin.register(UserShopProfile)
class UserShopProfileAdmin(admin.ModelAdmin):

    list_display = ('username', 'stripe_customer_id', 'count_of_products')

    @staticmethod
    def username(obj):
        return obj.user.username

    @staticmethod
    def stripe_customer_id(obj):
        return obj.customer_id

    @staticmethod
    def count_of_products(obj):
        return obj.product_checkouts.count()

