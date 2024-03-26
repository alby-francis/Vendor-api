from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..decorators import vendor_employee_login_required
from ..models import Product, Store, ProductAvailability
from ..serializers import ProductSerializer, ProductAvailabilitySerializer


@api_view(['GET'])
def get_all_products(request):
    try:
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@vendor_employee_login_required
def get_single_product(request, id):
    try:
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@vendor_employee_login_required
def add_product(request):
    try:
        # Check if the logged-in user is a supervisor
        logged_in_employee = request.current_user
        if logged_in_employee.role != 'supervisor':
            return Response({"message": "Only supervisors can add products"}, status=status.HTTP_403_FORBIDDEN)

        # Add unit_sold as 0 if not provided in request data
        request.data['unit_sold'] = 0

        # Save the product
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@vendor_employee_login_required
def delete_product(request, id):
    try:
        # Check if the logged-in user is a supervisor
        logged_in_employee = request.current_user
        if logged_in_employee.role != 'supervisor':
            return Response({"message": "Only supervisors can delete products"}, status=status.HTTP_403_FORBIDDEN)

        # Get the product to be deleted
        product = Product.objects.get(id=id)

        # Delete the product
        product.delete()

        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except Product.DoesNotExist:
        return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@vendor_employee_login_required
def get_single_store_product(request, store_id, product_id):
    try:
        # Check if the logged-in user is a supervisor
        logged_in_employee = request.current_user

        # Validate if store with provided store_id exists and belongs to the same vendor
        store = Store.objects.filter(id=store_id, vendor_id=logged_in_employee.vendor_id).first()
        if not store:
            return Response({"message": "Invalid store_id or store does not belong to the same vendor"},
                            status=status.HTTP_400_BAD_REQUEST)

        product = ProductAvailability.objects.get(product_id=product_id)
        serializer = ProductAvailabilitySerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"message": "Product not available in store"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@vendor_employee_login_required
def add_product_in_store(request, store_id, product_id):
    try:
        # Check if the logged-in user is a supervisor
        logged_in_employee = request.current_user
        if logged_in_employee.role != 'supervisor':
            return Response({"message": "Only supervisors can add product availability"},
                            status=status.HTTP_403_FORBIDDEN)

        # Validate if product with provided product_id exists
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"message": "Invalid product_id"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if store with provided store_id exists and belongs to the same vendor
        store = Store.objects.filter(id=store_id, vendor_id=logged_in_employee.vendor_id).first()
        if not store:
            return Response({"message": "Invalid store_id or store does not belong to the same vendor"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate request data
        serializer_data = {
            'store': store_id,
            'product': product_id,
            'price': request.data.get('price'),
            'total_unit': request.data.get('total_unit'),
            'unit_sold': 0
        }

        serializer = ProductAvailabilitySerializer(data=serializer_data)
        if serializer.is_valid():
            # Save the product availability entry
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@vendor_employee_login_required
def delete_product_in_store(request, store_id, product_id):
    try:
        # Check if the logged-in user is a supervisor
        logged_in_employee = request.current_user
        if logged_in_employee.role != 'supervisor':
            return Response({"message": "Only supervisors can delete product availability"},
                            status=status.HTTP_403_FORBIDDEN)

        # Validate if store with provided store_id exists and belongs to the same vendor
        store = Store.objects.filter(id=store_id, vendor_id=logged_in_employee.vendor_id).first()
        if not store:
            return Response({"message": "Invalid store_id or store does not belong to the same vendor"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate if product with provided product_id exists
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"message": "Invalid product_id"}, status=status.HTTP_400_BAD_REQUEST)


        # Check if the product availability entry exists
        product_availability = ProductAvailability.objects.filter(product_id=product_id, store_id=store_id).first()
        if not product_availability:
            return Response({"message": "Product availability not found"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the product availability entry
        product_availability.delete()

        return Response({"message": "Product availability deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    pass


@api_view(['GET'])
def get_all_products_in_store(request, store_id):
    try:
        # Query ProductAvailability objects for the given store_id
        product_availability = ProductAvailability.objects.filter(store_id=store_id).all()

        # Serialize the query result
        serializer = ProductAvailabilitySerializer(product_availability, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_product_availability_in_store(request, product_id):
    try:
        # Query ProductAvailability objects for the given product_id
        product_availability = ProductAvailability.objects.filter(product_id=product_id)

        # Serialize the query result
        serializer = ProductAvailabilitySerializer(product_availability, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_products_all_stores(request):
    try:
        # Get all stores
        stores = Store.objects.all()

        # Prepare dictionary to store products for each store
        all_products_all_stores = {}

        # Iterate through each store
        for store in stores:
            # Get products available in the current store
            products_in_store = ProductAvailability.objects.filter(store_id=store.id)

            # Serialize products available in the current store
            serialized_products = ProductAvailabilitySerializer(products_in_store, many=True).data

            # Store serialized products for the current store in the dictionary
            all_products_all_stores[store.name] = serialized_products

        return Response(all_products_all_stores, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT', 'PATCH'])
@vendor_employee_login_required
def update_product_availability(request, product_id,store_id):
    try:
        # Check if the logged-in user is a supervisor
        logged_in_employee = request.current_user
        if logged_in_employee.role != 'salesperson':
            return Response({"message": "Only salesperson can update product availability"}, status=status.HTTP_403_FORBIDDEN)

        # Get the product availability instance
        product_availability = ProductAvailability.objects.get(product_id=product_id,store_id=store_id)

        # Update unit_sold if provided in request data
        unit_sold = request.data.get('unit_sold')
        if unit_sold is not None:
            product_availability.unit_sold += unit_sold
            new_available_unit = product_availability.total_unit - unit_sold
            if new_available_unit < 0:
                return Response({"message": "Sold unit cannot be larger tha available unit"}, status=status.HTTP_403_FORBIDDEN)
            product_availability.total_unit = new_available_unit
            product_availability.save()

            # Serialize and return the updated product availability
            serializer = ProductAvailabilitySerializer(product_availability)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "unit_sold field is required"}, status=status.HTTP_400_BAD_REQUEST)

    except ProductAvailability.DoesNotExist:
        return Response({"message": "Product availability not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)