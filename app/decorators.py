from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import CustomerUser, VendorEmployee
import jwt


def customer_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return Response({"message": "Token is missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode the token
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
            user_id = payload.get('user_id')

            # Retrieve the user from the database
            user = CustomerUser.objects.get(id=user_id)

            # Attach the user object to the request
            request.current_user = user

            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomerUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    return wrapper

def vendor_employee_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if 'Bearer ' in token:
            token = token.replace('Bearer ','')
        if not token:
            return Response({"message": "Token is missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode the token
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
            user_id = payload.get('user_id')

            # Retrieve the user from the database
            user = VendorEmployee.objects.get(id=user_id)

            # Attach the user object to the request
            request.current_user = user

            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except VendorEmployee.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    return wrapper