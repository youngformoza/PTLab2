from django.db import models


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    # products = models.ManyToManyField('Product', related_name='promo_codes')


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    promo_codes = models.ManyToManyField(PromoCode, through='ProductPromoCodeRelation', related_name='products')


class ProductPromoCodeRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
