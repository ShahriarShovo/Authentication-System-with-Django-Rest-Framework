from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers
from accounts.models import User
from accounts.models import Profile
from rest_framework import status
from rest_framework.response import Response



class UserRegistrationSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'})
    class Meta:
        model = User
        fields = ['email','password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Password and Confirm Password Doesnt match')
        else:
            return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model=User
        fields=['email','password']



class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields=['username', 'full_name', 'address', 'city', 'zipcode', 'country', 'phone']


class User_Password_Change_Serializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
       
        fields=['password','confirm_password']

    def validate(self, attrs):
        password= attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        user = self.context.get('user')
        if password != confirm_password :
            raise ValueError('Password Doesnt match')
        else:
            user.set_password(password)
            user.save()
            return attrs      



# class UserPasswordChangedSerializer(serializers.Serializer):
#     password = serializers.CharField(style={'input_type':'password'}, write_only=True)
#     confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)

#     class Meta:
#         fields = ['password','confirm_password']

#     def validate(self, attrs):
#         password = attrs.get('password')
#         confirm_password = attrs.get('confirm_password')
#         user=self.context.get('user')
#         if password != confirm_password:
#             raise ValidationError("Password Doesn't match")
#         user.set_password(password)
#         user.save()
#         return attrs


        