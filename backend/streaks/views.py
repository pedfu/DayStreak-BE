from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

class CategoriesViewSet(generics.ListCreateAPIView):
    queryset = StreakCategory.objects.all()
    serializer_class = CategoriesSerializer

class CategoryViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = CategorySerializer(data=request.data, context={ 'user': user })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserStreaksView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = StreakSerializer(data=request.data, context={ 'user': user })
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        user_streaks = UserStreak.objects.filter(user=user)
        serializer = UserStreakSerializer(user_streaks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StreakTrackView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = UserStreakCountSerializer(data=request.data, context={ 'user': user })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class StreakTrackDetailsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        user = request.user
        streak = Streak.objects.filter(id=id).first()
        user_streak = UserStreak.objects.filter(user=user, streak=streak).first()
        
        if user_streak:
            serializer = UserStreakDetailsCountSerializer(
                instance=user_streak, 
                data={'user':user_streak.user.id, 'streak':user_streak.streak.id, 'category': user_streak.category.id}
            )
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
