from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        
        ('administrator', 'Administrator'),
        
    ]
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='farmer_profile')
    farm_size = models.FloatField(blank=True, null=True)  
    farm_type = models.CharField(max_length=100, blank=True, null=True)  
    crops_grown = models.TextField(blank=True, null=True)  

 
    
   
class AdministratorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='admin_profile')
    department = models.CharField(max_length=255, blank=True, null=True)
    admin_level = models.IntegerField(default=1) 





@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  
    if created:
        if instance.role == 'farmer':
            FarmerProfile.objects.create(user=instance)
        elif instance.role == 'administrator':
            AdministratorProfile.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
   
    if instance.role == 'farmer' and hasattr(instance, 'farmer_profile'):
        instance.farmer_profile.save()
    elif instance.role == 'administrator' and hasattr(instance, 'admin_profile'):
        instance.admin_profile.save()
   



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.product.price