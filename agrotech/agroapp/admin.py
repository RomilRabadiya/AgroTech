

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FarmerProfile, AdministratorProfile

# Register custom User model
admin.site.register(User, UserAdmin)

# Register additional profiles
admin.site.register(FarmerProfile)

admin.site.register(AdministratorProfile)

from django.contrib import admin
from .models import Category, Product, Order

# Register models so they appear in Django Admin
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)