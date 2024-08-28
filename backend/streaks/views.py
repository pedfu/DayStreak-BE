from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import QueryDict

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

    def get(self, request):
        user = request.user
        categories = StreakCategory.objects.filter(user=user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CategoryDeleteViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        category = StreakCategory.objects.filter(id=id).first()
        if category is not None and category.user.id == user.id:
            user_streaks = UserStreak.objects.filter(category__id=category.id, user__id=user.id)
            streaks_id = user_streaks.values_list('streak__id', flat=True)
            Streak.objects.filter(id__in=streaks_id).delete()
            user_streaks.delete()
            category.delete()
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_400_BAD_REQUEST)
    
class StreakDeleteViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        streak = Streak.objects.filter(id=id).first()
        if streak is not None:
            user_streaks = UserStreak.objects.filter(streak__id=streak.id, user__id=user.id)
            user_streaks.delete()
            if streak.created_by.id == user.id:
                streak.delete()
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_400_BAD_REQUEST)

class UserStreaksView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data.get('data')
        background = request.data.get('background')
        if isinstance(data, QueryDict):
            data = data.dict()
        else:
            data = json.loads(data)
        serializer = StreakSerializer(data=data, context={ 'user': user, 'background': background })
        if serializer.is_valid():
            serializer.save()       
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            data = json.loads(request.data.get('data'))
            user = request.user
            streak = Streak.objects.get(id=id)
            user_streak = UserStreak.objects.get(streak__id=streak.id, user__id=user.id)
            serializer = StreakSerializer(user_streak, data=data, context={'user': request.user, 'background': request.data.get('background')})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('error', e)

    def get(self, request):
        user = request.user
        user_streaks = UserStreak.objects.filter(user=user)
        serializer = UserStreakSerializer(user_streaks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        user = request.user
        streak = Streak.objects.filter(id=id).first()
        if streak is not None and user == streak.created_by:
            streak.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
    
class UserStreakDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        user_streak = UserStreak.objects.get(id=id)
        serializer = StreakSerializer(user_streak, data=request.data, context={'user': request.user, 'background': request.data.get('background')})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
