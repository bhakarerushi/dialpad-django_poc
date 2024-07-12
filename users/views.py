from rest_framework import viewsets, permissions
from rest_framework.response import Response
from users.models import PlatformUser, Post
from users.serializers import (PlatFormUserUpdateSerializer, PlatFormUserSerializer,PostCreateSerializer, 
                               PostSerializer)
from users import logger
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.custom_permissions import IsStaffUSerReadOnly
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

import requests
from django.conf import settings
from social_django.utils import psa
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import permission_classes
from test_package import test_method



class LoginUserViewSet(viewsets.ViewSet):

    # @action(detail=True, methods=['POST'])
    def login(self,request):
        print("data", request.data)
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        logger.debug("user login")
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
                samesite='strict',  # Set according to your needs
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
    pagination_class = LimitOffsetPagination  # Apply the custom pagination class

    permission_classes = [IsStaffUSerReadOnly]

    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         permission_classes = [permissions.IsAuthenticated]
    #     elif self.action in ['update', 'partial_update', 'destroy']:
    #         permission_classes = [permissions.IsAdminUser]
    #     print("permission classes", permission_classes)
    #     return [permission() for permission in permission_classes]
    

    def list(self, request):
        queryset = PlatformUser.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = PlatFormUserSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = PlatFormUserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    

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
    pagination_class = LimitOffsetPagination  # Apply the custom pagination class



    def get_queryset(self):
        if self.request.user.is_staff:
            qs = Post.objects.filter(created_by=self.request.user)
        else:
            qs = Post.objects.all()
        return qs

    def list(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

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

    # @psa('social:complete')
    def get(self, request):
        code = request.GET.get('code')
        client_id = settings.SOCIAL_AUTH_GITHUB_KEY
        client_secret = settings.SOCIAL_AUTH_GITHUB_SECRET

        # Exchange code for access token
        token_response = requests.post('https://github.com/login/oauth/access_token', data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code
        }, headers={'Accept': 'application/json'})
        
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        print("access_token", access_token)
        # if not access_token:
        #     return Response({'error': 'Failed to obtain access token'}, status=status.HTTP_400_BAD_REQUEST)
        #  # Authenticate and create user
        # user = request.backend.do_auth(access_token)

        headers = {
                    'Accept': 'application/vnd.github+json',
                    'Authorization': 'Bearer {}'.format(access_token),
                    'X-GitHub-Api-Version': '2022-11-28',
                }

        response = requests.get('https://api.github.com/user', headers=headers)

        return Response(response.json())
        if user:
            return Response("login in sucess with user creation", status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)
        


class TestView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    # @psa('social:complete')
    def get(self, request):
        print("user_perm", permissions.IsAuthenticated.has_permission(self, request, None))
        print("user obj", request.user._meta.get_fields())
        print("user dict", request.user.__dict__.keys())
        if request.user.is_staff :
            return Response({"data":"Hello user !!"})
        return Response({"data":"Hello Admin !!"})