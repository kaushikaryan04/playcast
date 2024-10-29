from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import *

class RegistrationSerializer(serializers.ModelSerializer) :
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required = True ,
        write_only = True ,
        validators = [validate_password]
    )
    password2 = serializers.CharField(write_only = True , required = True )

    class Meta :
        model = User
        fields = ['username','password','email','first_name','last_name' , 'password2']

    def validate(self, attrs) :
        if attrs['password'] != attrs['password2'] :
            raise serializers.ValidationError({'password' : 'Passwords do not match please try again'})
        return attrs

    def create(self , validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class VideoSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Video
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = ['id' , 'email' , 'username' , 'first_name' , 'last_name']
