from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from ..serializers import CustomerUserSerializer
from ..models import CustomerUser
from ..utils import valid_password, valid_first_name, valid_last_name
import jwt
import datetime
# Create your views here.

@csrf_exempt
@api_view(['GET'])
def user(request):
    customers = CustomerUser.objects.all()
    serializer = CustomerUserSerializer(customers,many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def createUser(request):
    data = request.data
    try:
        customer = CustomerUser.objects.get(email=data["email"])
        if customer:
            return Response({"message": "Email already in use"})
    except:
        pass
    if not valid_password(data["password"]):
        return Response({"message" : "password doesn't meet minimum requirement"})
    if not valid_first_name(data["first_name"]):
        return Response({"message" : "Invalid first name"})
    if not valid_last_name(data["last_name"]):
        return Response({"message" : "Invalid last name"})
    # Encode password with JWT
    encoded_password = jwt.encode({'password': data["password"]}, 'secret_key', algorithm='HS256')
    data["password"] = encoded_password
    serializer = CustomerUserSerializer(data=data)
    if serializer.is_valid():
        user_instance  = serializer.save()
        # token expire after 7 days
        login_token = jwt.encode({'user_id': serializer.data["id"],
                                  'expire':(datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()},
                                 'secret_key', algorithm='HS256')
        user_instance.login_token = login_token
        user_instance.save()
        return_data = serializer.data
        return_data['login_token'] = login_token
        return Response(return_data)
    return Response({"message": "more information is required. Data not saved"})

@csrf_exempt
@api_view(['DELETE'])
def removeUser(request,id):

    # Find user with email and encoded password
    customer = get_object_or_404(CustomerUser, id=id )
    customer.delete()
    return Response({"message": "User deleted successfully."})

@csrf_exempt
@api_view(['POST'])
def user_login(request):
    data = request.data
    # Encode password with JWT
    encoded_password = jwt.encode({"password": data["password"]}, 'secret_key', algorithm='HS256')

    # Find user with email and encoded password
    customer = get_object_or_404(CustomerUser, email=data["email"], password=encoded_password)
    if customer:
        serializer = CustomerUserSerializer(customer)

        # Generate login token
        login_token = jwt.encode({'user_id': serializer.data["id"],
                                  'expire': (datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()},
                                 'secret_key', algorithm='HS256')

        # Update login token in user instance
        customer.login_token = login_token
        customer.save()

        # Include login token in response data
        return_data = serializer.data
        return_data['login_token'] = login_token
        return Response({'message': "authenticated", "user_data": return_data})
    return Response({"message": "Invalid email/password."})

