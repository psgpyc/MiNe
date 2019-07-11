from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import PermissionDenied


from .managers import (
    ProductManager,
    )

from coremodels.models import (
    RelatedProductColors,
    RelatedProductTypes)

from django.utils.text import slugify


def upload_productimage_path(self, filename):
    return 'product_images/{category}/{name}/{filename}'.format(
        category=self.category,
        name=self.name,
        filename=filename)


class Catalog(models.Model):
    MAJOR_CATALOG = [
        ('sig', 'Signature Products'),
        ('ant', 'Antiques'),
        ('A&C', 'Arts and Crafts'),
        ('BeR', 'Better Replacement'),
        ('cul', 'Cultural'),
        ('dec', 'Decor'),
        ('G&J', 'Gems and Jewellery'),
        ('hrb', 'Herbals'),
        ('NaF', 'Natural Fabrics'),
        ('let', 'Leather'),
        ('sou', 'Souvenir'),
        ('mus', 'Musical Instruments'),

    ]
    name = models.CharField(max_length=100, unique=True,
                            blank=False, null=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField()
    major_catalog = models.CharField(
        max_length=3, choices=MAJOR_CATALOG, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Catalog, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Catalog'
        verbose_name = 'Catalog'


class Products(models.Model):
    name = models.CharField(help_text='Input product name',
                            max_length=255, verbose_name='Product Name')
    materialDescription = models.TextField(
        help_text='Input product material description',
        verbose_name='Product Description')
    catalog_category = models.ForeignKey(
        Catalog,
        verbose_name='Category',
        help_text='Product associated Category defined on the Catalog',
        on_delete=models.CASCADE)
    product_image = models.ImageField(
        upload_to=upload_productimage_path,
        verbose_name='Product Image',
        help_text='Input products image',
        null=True,
        blank=True)
    slug = models.SlugField(max_length=100, editable=False, unique=True)
    relatedType = models.ManyToManyField(
        RelatedProductTypes,
        verbose_name='Related Product Type',
        help_text='Input related product type',
    )
    color = models.ManyToManyField(
        RelatedProductColors,
        help_text=' A products color',
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='A products price'
    )
    weight = models.FloatField(
        help_text='A products weight'

    )
    size = models.CharField(
        max_length=255,
        help_text='A products Size',
        blank=True,
        null=True)
    is_available = models.BooleanField(
        default=True,
        help_text='A product is available in Inventory'
    )
    has_offer_value = models.BooleanField(
        default=False,
        help_text='A product is on sale or has an offer'

    )

    objects = ProductManager()

    def __str__(self):
        return self.name

    def price_with_promo(self, promo_code):
        if self.has_offer_value:
            return self.price-(self.price * promo_code.code_percentage / 100)
        else:
            return self.price

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Products'
        verbose_name = 'Product'


class ProductImages(models.Model):
    product_name = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to=upload_productimage_path, null=True, blank=True)

    def __str__(self):
        return self.product_name.name

    class Meta:
        verbose_name_plural = 'Product Images'
        verbose_name = 'Product Image'


class PromoCode(models.Model):
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE)

    code = models.CharField(
        max_length=100,
        unique=True,
        editable=False,
        blank=True,
        null=True)
    usage_limit = models.IntegerField(default=0)

    expiring_date = models.DateTimeField()

    code_percentage = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)])

    def save(self, *args, **kwargs):
        if self.pk:
            raise PermissionDenied
        pro_name = self.product.name.split()
        self.code = pro_name[0][:3].lower() + \
            str(self.code_percentage) + \
            pro_name[-1][:3].lower()
        super(PromoCode, self).save(*args, **kwargs)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'PromoCodes'
