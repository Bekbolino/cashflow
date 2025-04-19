from django.utils import timezone
from django.db import models

# models.py

# Статус
class Status(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

# Тип
class Type(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

# Категория
class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

# СубКатегория
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name
# Транзакция
class CashFlow(models.Model):

    date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.custom_date}  - {self.status} - {self.type} - {self.category} - {self.subcategory} - {self.amount} "

# Create your models here.
