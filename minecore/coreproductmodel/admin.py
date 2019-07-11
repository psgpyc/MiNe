from django.contrib import admin
from .models import (
    Catalog,
    Products,
    ProductImages,
    PromoCode
)

admin.site.register(Catalog)
admin.site.register(Products)
admin.site.register(ProductImages)
admin.site.register(PromoCode)
