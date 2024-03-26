from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import render

@csrf_exempt
@api_view(['GET'])
def check_health(request):
    return render(request, 'health.html')
    #return Response({"message": "Server is up"})