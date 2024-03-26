from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import Store
from ..serializers import StoreSerializer
from ..decorators import vendor_employee_login_required


@api_view(['GET'])
def get_all_stores(request):
    try:
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@vendor_employee_login_required
def add_store(request):
    try:
        # Get the logged-in employee
        logged_in_employee = request.current_user

        # Check if the logged-in employee is an admin
        if logged_in_employee.role != 'admin':
            return Response({"message": "Only admin can add a store"}, status=status.HTTP_403_FORBIDDEN)

        # assign logged user vendor id to new user - as they will be in same vendor org
        data = request.data
        data['vendor'] = logged_in_employee.vendor_id

        # Serialize the request data
        serializer = StoreSerializer(data=data)

        # Validate the serializer data
        if serializer.is_valid():
            # Save the store data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@vendor_employee_login_required
def get_single_store(request, id):
    try:
        store = Store.objects.get(id=id)
        serializer = StoreSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Store.DoesNotExist:
        return Response({"message": "Store not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@vendor_employee_login_required
def delete_store(request, id):
    try:
        # Get the logged-in employee
        logged_in_employee = request.current_user

        # Get the employee to be deleted
        store = Store.objects.get(id=id)

        # Check if both store and current user belong to the same vendor
        if logged_in_employee.vendor_id != store.vendor_id:
            return Response({"message": "Store/Employee do not belong to the same vendor"},
                            status=status.HTTP_403_FORBIDDEN)

        # Check if the logged-in employee is an admin
        if logged_in_employee.role != 'admin':
            return Response({"message": "Only admin can delete store"}, status=status.HTTP_403_FORBIDDEN)

        # Delete the employee
        store.delete()

        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Store.DoesNotExist:
        return Response({"message": "Store not found"}, status=status.HTTP_404_NOT_FOUND)