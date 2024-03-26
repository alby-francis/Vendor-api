from django.db import models

# Create your models here.
class CustomerUser(models.Model):
    email = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    login_token = models.CharField(max_length=256, default='null')
    def __str__(self):
        return '<user: '+str(self.email)+'>'


class Vendor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return '<vendor: '+str(self.name)+'>'


class VendorEmployee(models.Model):
    ROLES = (
        ('admin', 'Admin'),
        ('supervisor', 'Supervisor'),
        ('salesperson', 'Salesperson'),
    )

    email = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    login_token = models.CharField(max_length=256, default='null')
    role = models.CharField(max_length=20, choices=ROLES)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return '<email: '+str(self.email) + ', role: ' + str(self.role)+'>'


class Store(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return '<store: '+str(self.name)+'>'


class Product(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)


    def __str__(self):
        return '<product: '+str(self.name)+'>'

class ProductAvailability(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    total_unit = models.IntegerField(default=0)
    unit_sold = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '<product: '+str(self.product) + ', store: ' +str(self.store)+'>'