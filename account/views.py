from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


@api_view(['GET'])
@permission_classes([permissions.AllowAny], )
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
    print(serializer.data)
    return Response(serializer.data)


class UserList(APIView):
	permission_classes = (permissions.AllowAny,)

	def post(self, request, format=None):
		serializer = UserSerializerWithToken(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	    



				