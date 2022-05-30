from multiprocessing import context
from django.contrib.auth import login, logout, authenticate
from yaml import serialize
from accounts.models import Profile, User
from accounts.serializers import (UserRegistrationSerializers, 
LoginSerializer,ProfileSerializer,User_Password_Change_Serializer)
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class Signup_user(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token = get_tokens_for_user(user)
            return Response({'message':'Signup Successful', 'token':token}, status=status.HTTP_201_CREATED)
        return Response({'message':'Signup Failed'}, status=status.HTTP_400_BAD_REQUEST)



class User_login(APIView):
    def post(self,request):
        form = LoginSerializer(data=request.data)
        if form.is_valid():
            email=form.data.get('email')
            password=form.data.get('password')
            user=authenticate(email=email, password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'message':'Login Successfull', 'token':token}, status=status.HTTP_200_OK)
            else:
                return Response({'message':'User no Found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'message':'User no Found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    Profile_serializer = ProfileSerializer(profile) 
    return Response(Profile_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request, user_id):
    try:
        print('request  data = ', request.data)
        profile = Profile.objects.get(user__id=user_id)
        update_serializer=ProfileSerializer(profile, data=request.data)
        
        if update_serializer.is_valid():
            update_serializer.save(user=request.user)
            return Response(update_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'message':'error'})

    except Exception as e:
        print(e)
        return Response({'message':'Data is not Valided'})



class User_Change_Password(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        serialize = User_Password_Change_Serializer(data=request.data, context={'user':request.user})
        if serialize.is_valid():
            return Response({'message':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Failed to Change Password'}, status=status.HTTP_400_BAD_REQUEST)
            



# class UserPasswordChangedView(APIView):
#     def post(self, request, format=None):
#         permission_classes=[IsAuthenticated]
#         serializer = UserPasswordChangedSerializer(data=request.data, context={'user':request.user})
#         if serializer.is_valid(raise_exception=True):
#             return Response({'message':'Password Changed Successfully'}, status=status.HTTP_200_OK)
#         return Response({'message':'Failed to Change Password'}, status=status.HTTP_400_BAD_REQUEST)










          
