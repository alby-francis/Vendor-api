from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt
from django.shortcuts import get_object_or_404

from ..decorators import vendor_employee_login_required
from ..models import Vendor, VendorEmployee
from ..serializers import VendorSerializer, VendorEmployeeSerializer
import datetime


@csrf_exempt
@api_view(['GET'])
def get_all_vendors(request):
    customers = Vendor.objects.all()
    serializer = VendorSerializer(customers,many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def get_all_vendor_employees(request):
    customers = VendorEmployee.objects.all()
    serializer = VendorEmployeeSerializer(customers,many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
@vendor_employee_login_required
def create_employee(request):
    logged_in_employee = request.current_user

    # Check is logged user is admin
    if logged_in_employee.role != "admin":
        return Response({"message": "Only admin employees can create new employees"}, status=status.HTTP_403_FORBIDDEN)

    data = request.data

    # Check if email is already in use
    try:
        vendor = VendorEmployee.objects.get(email=data["email"])
        if vendor:
            return Response({"message": "Email already in use for vendor employee"}, status=status.HTTP_400_BAD_REQUEST)
    except VendorEmployee.DoesNotExist:
        pass

    # Encode password with JWT
    encoded_password = jwt.encode({'password': data["password"]}, 'secret_key', algorithm='HS256')
    data['password'] = encoded_password

    # assign logged user vendor id to new user - as they will be in same vendor org
    data['vendor'] = logged_in_employee.vendor_id

    serializer = VendorEmployeeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def create_vendor_with_employee(request):
    data = request.data

    try:
        vendor = VendorEmployee.objects.get(email=data["email"])
        if vendor:
            return Response({"message": "Email already in use for vendor employee"}, status=status.HTTP_400_BAD_REQUEST)
    except VendorEmployee.DoesNotExist:
        pass

    # admin details are provided
    if "first_name" not in data or "last_name" not in data or "email" not in data or "password" not in data:
        return Response({"message": "all admin details are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a vendor
    vendor_serializer = VendorSerializer(data=data)
    if vendor_serializer.is_valid():
        vendor_instance = vendor_serializer.save()
    else:
        return Response({"message": "More information is required for vendor creation"},
                        status=status.HTTP_400_BAD_REQUEST)


    # Create an employee with admin role
    employee_data = {
        "email": data["email"],
        "password": data["password"],
        "role": "admin",
        "vendor": vendor_instance.id,  # Assign the vendor to the employee
        "first_name": data["first_name"],  # Add first_name to employee data
        "last_name": data["last_name"]     # Add last_name to employee data
    }
    employee_serializer = VendorEmployeeSerializer(data=employee_data)
    if employee_serializer.is_valid():
        employee_instance = employee_serializer.save()
    else:
        # Rollback vendor creation if employee creation fails
        vendor_instance.delete()
        return Response({"message": "More information is required for employee creation"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Encode password with JWT
    encoded_password = jwt.encode({'password': data["password"]}, 'secret_key', algorithm='HS256')
    employee_instance.password = encoded_password
    employee_instance.save()

    # Generate login token for the employee
    login_token = jwt.encode({'user_id': employee_instance.id,
                              'expire': (datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()},
                             'secret_key', algorithm='HS256')
    employee_instance.login_token = login_token
    employee_instance.save()

    # Return response
    response_data = {
        "vendor": vendor_serializer.data,
        "employee": employee_serializer.data,
    }
    return Response(response_data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['GET'])
@vendor_employee_login_required
def get_employee(request, id):

    try:
        # Get the logged-in employee
        logged_in_employee = request.current_user

        # Get the employee
        employee = VendorEmployee.objects.get(id=id)

        # Check if both employees belong to the same vendor
        if logged_in_employee.vendor_id != employee.vendor_id:
            return Response({"message": "Employee does not belong to the same vendor"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = VendorEmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except VendorEmployee.DoesNotExist:
        return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@vendor_employee_login_required
@api_view(['PUT'])
def edit_employee_role(request, id):
    try:
        logged_in_employee = request.current_user
        employee = VendorEmployee.objects.get(id=id)

        # Check if both employees belong to the same vendor
        if logged_in_employee.vendor_id != employee.vendor_id:
            return Response({"message": "Both employees do not belong to the same vendor"}, status=status.HTTP_403_FORBIDDEN)

        if logged_in_employee.role != 'admin':
            return Response({"message": "Only admin can edit employee roles"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        if 'role' not in data:
            return Response({"message": "Role field is required"}, status=status.HTTP_400_BAD_REQUEST)

        new_role = data['role']
        if new_role not in ['admin', 'supervisor', 'salesperson']:
            return Response({"message": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        employee.role = new_role
        employee.save()

        serializer = VendorEmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except VendorEmployee.DoesNotExist:
        return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
def employee_login(request):
    data = request.data
    # Encode password with JWT
    encoded_password = jwt.encode({"password": data["password"]}, 'secret_key', algorithm='HS256')

    # Find employee with email and encoded password
    employee = get_object_or_404(VendorEmployee, email=data["email"], password=encoded_password)
    if employee:
        serializer = VendorEmployeeSerializer(employee)

        # Generate login token
        login_token = jwt.encode({'user_id': serializer.data["id"],
                                  'expire': (datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()},
                                 'secret_key', algorithm='HS256')

        # Update login token in employee instance
        employee.login_token = login_token
        employee.save()

        # Include login token in response data
        return_data = serializer.data
        return_data['login_token'] = login_token
        return Response({'message': "Authenticated", "user_data": return_data})
    return Response({"message": "Invalid email/password."}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
@api_view(['DELETE'])
@vendor_employee_login_required
def delete_employee(request, id):
    try:
        # Get the logged-in employee
        logged_in_employee = request.current_user

        # Get the employee to be deleted
        employee = VendorEmployee.objects.get(id=id)

        # Check if both employees belong to the same vendor
        if logged_in_employee.vendor_id != employee.vendor_id:
            return Response({"message": "Both employees do not belong to the same vendor"}, status=status.HTTP_403_FORBIDDEN)

        # Check if the logged-in employee is an admin
        if logged_in_employee.role != 'admin':
            return Response({"message": "Only admin can delete employees"}, status=status.HTTP_403_FORBIDDEN)

        # Delete the employee
        employee.delete()

        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except VendorEmployee.DoesNotExist:
        return Response({"message": "Store not found"}, status=status.HTTP_404_NOT_FOUND)