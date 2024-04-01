from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

# Create your views here.
class CategoriesViewSet(generics.ListCreateAPIView):
    queryset = StreakCategory.objects.all()
    serializer_class = CategoriesSerializer

class UserStreaksView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = StreakSerializer(data=request.data, context={ 'user': user })
        print('teste')
        if serializer.is_valid():
            print('valid')
            serializer.save()
        else:
            print('invalid')
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        user_streaks = UserStreak.objects.filter(user=user)
        serializer = UserStreakSerializer(user_streaks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
