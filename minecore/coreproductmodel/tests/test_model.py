from django.test import TestCase
from django.utils import timezone
from coremodels.models import (
    RelatedProductColors,
    RelatedProductTypes)

from .. import models


class ProductModelTests(TestCase):

    def setUp(self):
        self.related_color = RelatedProductColors.objects.create(
            name="Red"
        )

        self.related_type = RelatedProductTypes.objects.create(
            name='Cotton'
        )

        self.product_catalog = models.Catalog.objects.create(
            name='woodcraft',
            description='This is a simple woodcraft',
            major_catalog='A&C',

        )
        self.product = models.Products.objects.create(
            name='wood photo frame',
            materialDescription='oak wood',
            catalog_category=self.product_catalog,
            price=400,
            weight=0.54,
            size='29.7*21',
            is_available=True,
            has_offer_value=False,
        )
        self.product.relatedType.set([self.related_type])
        self.product.color.set([self.related_color])

        self.product_image = models.ProductImages.objects.create(
            product_name=self.product)

        self.promo_code = models.PromoCode.objects.create(
            product=self.product,
            usage_limit=5,
            expiring_date=timezone.now(),
            code_percentage=30,
        )

    def test_catalog_str(self):
        self.assertEqual(str(self.product_catalog), self.product_catalog.name)

    def test_catalog_verbose_name(self):
        self.assertEqual(models.Catalog._meta.verbose_name, "Catalog")
        self.assertEqual(models.Catalog._meta.verbose_name_plural, "Catalog")

    def test_product_str(self):
        self.assertEqual(str(self.product), self.product.name)

    def test_product_verbose_name(self):
        self.assertEqual(models.Products._meta.verbose_name, 'Product')
        self.assertEqual(models.Products._meta.verbose_name_plural, 'Products')

    def test_product_image_str(self):
        self.assertEqual(
            str(self.product_image),
            self.product_image.product_name.name)

    def test_product_image_verbose_name(self):
        self.assertEqual(
            models.ProductImages._meta.verbose_name,
            'Product Image')
        self.assertEqual(
            models.ProductImages._meta.verbose_name_plural,
            'Product Images')

    def test_promo_code_str(self):
        self.assertEqual(str(self.promo_code), self.promo_code.code)

    def test_promo_code_verbose_name(self):
        self.assertEqual(
            models.PromoCode._meta.verbose_name_plural,
            'PromoCodes')

    def test_promo_code_code(self):
        self.assertEqual(str(self.promo_code.code), 'woo30fra')
