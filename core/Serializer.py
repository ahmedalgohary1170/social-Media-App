
from rest_framework import serializers
from .models import Post , Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','id']
        
        


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()    
    class Meta:
        model = Profile
        exclude = ['id_user']
        
         



class Postserializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'