from rest_framework import serializers
from .models import CustomerUser, Vendor, VendorEmployee, Store, Product, ProductAvailability


class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class VendorEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorEmployee
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAvailability
        fields = '__all__'