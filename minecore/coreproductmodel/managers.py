from django.db import models


class ProductQuerySets(models.QuerySet):
    pass


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySets(self.model, using=self._db)
