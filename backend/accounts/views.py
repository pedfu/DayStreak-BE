from .models import *
from streaks.models import UserStreak, Streak
from .serializers import *
from streaks.serializers import BadgeSerializer, StreakSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            token, _ = Token.objects.get_or_create(user=user)
            token_user_serializer = TokenUserSerializer(token)
            return Response(token_user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data.get('username_or_email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                token_user_serializer = TokenUserSerializer(token)
                return Response(token_user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            token = request.headers.get('Authorization').split()[1]
        except:
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Token.objects.get(key=token).delete()
            return Response({'success': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class UserBadgesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        badges = user.badges.all()

        serializer = BadgeSerializer(badges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserNotificationsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)

        serializer = NotificationsSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReadNotificationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user        
        notification = Notification.objects.filter(id=id, user=user).first()
        if notification:
            notification.read = True
            notification.save()
            return Response(status=status.HTTP_200_OK)
        return Response({ 'error': 'Notification not found' }, status=status.HTTP_404_NOT_FOUND)