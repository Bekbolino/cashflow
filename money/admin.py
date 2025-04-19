from django.contrib import admin
from money.models import *

admin.site.register(CashFlow)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Category)
admin.site.register(SubCategory)

# Register your models here.
