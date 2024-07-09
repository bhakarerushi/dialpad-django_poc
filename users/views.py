from rest_framework import viewsets, permissions
from rest_framework.response import Response
from users.models import PlatformUser, Post
from users.serializers import (PlatFormUserUpdateSerializer, PlatFormUserSerializer,PostCreateSerializer, 
                               PostSerializer)
from users import logger
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.custom_permissions import IsStaffUSer
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView



class LoginUserViewSet(viewsets.ViewSet):

    # @action(detail=True, methods=['POST'])
    def login(self,request):
        print("data", request.data)
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        print("user", user)
        if user:
            refresh = RefreshToken.for_user(user=user)
            tokens = {
                "refresh":str(refresh),
                "access": str(refresh.access_token)
            }
            print("tokens", tokens)
            response = Response(data=tokens, status=status.HTTP_200_OK)
        
            response.set_cookie(
                'refresh_token', 
                tokens['refresh'], 
                httponly=True, 
                secure=False,  # Set to False for development, True for production
                samesite='Lax',  # Set according to your needs
                max_age=60*5 
            )
            return response

        return Response(data={"user not found"},status=status.HTTP_401_UNAUTHORIZED)

    def signup(self, request):
        data = request.data
        serialzier = PlatFormUserSerializer(data=data)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data, status.HTTP_201_CREATED)
        return Response(data=serialzier.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class TokenRefreshViewSet(viewsets.ViewSet, TokenRefreshView):

    def token_refresh(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        request.data['refresh'] = refresh_token
        response = super().post(request)
        print(response)
        if response.status_code == status.HTTP_200_OK:
            response.set_cookie(
                'refresh_token', 
                response.data['refresh'], 
                httponly=True, 
                secure=False,  # Set to False for development, True for production
                samesite='Lax',  # Set according to your needs
                max_age=60*10 
            )
            return response
        
        return response.data



class PlatFormUserViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            print("staff user")
            permission_classes = [permissions.IsAdminUser, IsStaffUSer]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    
    def list(self, request):
        qs = PlatformUser.objects.all()
        logger.info("inside view func ")
        serialzier = PlatFormUserSerializer(qs, many=True)
        return Response(serialzier.data)

    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        serialzier = PlatFormUserSerializer(user)
        return Response(serialzier.data)

    
    def partial_update(self, request, pk=None):
        user = self.get_object(pk)
        data = request.data
        logger.info("data", data)
        serialzier = PlatFormUserUpdateSerializer(user, data=data, partial=True)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data, status.HTTP_200_OK)
        return Response(data=serialzier.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self,pk=None):
        user = PlatformUser.objects.get(pk=pk)
        return user
    
    def destroy(self, request, pk=None):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_200_OK)
    

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        if self.request.user.is_staff:
            qs = Post.objects.filter(created_by=self.request.user)
        else:
            qs = Post.objects.all()
        return qs

    def list(self, request):
        qs = self.get_queryset()
        qs = qs.filter(created_by=request.user)
        serialzier = PostSerializer(qs, many=True)
        return Response(serialzier.data)

    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        serialzier = PostSerializer(user)
        return Response(serialzier.data)
    
    def create(self, request):
        data = request.data
        serialzier = PostCreateSerializer(data=data)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data, status.HTTP_201_CREATED)
        return Response(data=serialzier.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def partial_update(self, request, pk=None):
        user = self.get_object(pk)
        data = request.data
        serialzier = PostCreateSerializer(user, data=data, partial=True)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data, status.HTTP_200_OK)
        return Response(data=serialzier.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_200_OK)

    def get_object(self,pk=None):
        users = Post.objects.filter(pk=pk)
        user = get_object_or_404(users, pk=pk)
        return user
    

class OauthGitHubView(APIView):

    def get(self, request):
        print("params", request.GET)
        return Response(status=status.HTTP_200_OK)