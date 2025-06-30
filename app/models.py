from django.db import models
from django.contrib.auth.models import User
# Create your models here.

PROVINCE_CHOICES = (
('Eastern Cape', 'Eastern Cape'),    
('Free State', 'Free State'),
('Gauteng', 'Gauteng'),
('KwaZulu-Natal', 'KwaZulu-Natal'),
('Limpopo', 'Limpopo'),
('Mpumalanga', 'Mpumalanga'),
('Northern Cape', 'Northern Cape'),
('North West', 'North West'),
('Western Cape', 'Western Cape'),
)

CATEGORY_CHOICES=(
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('MS','Milkshake'),
    ('PN','Paneer'),
    ('GH','Ghee'),
    ('CZ','Cheese'),
    ('IC','Ice-Creams'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.tittle
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200) 
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=PROVINCE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
      