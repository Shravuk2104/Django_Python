from django.contrib import admin
from estoreapp.models import product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id', 'name','price','pdetails','cat','is_active']
    list_filter=['price','cat','is_active']





admin.site.register(product,ProductAdmin)