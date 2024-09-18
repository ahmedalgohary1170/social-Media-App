from rest_framework import generics
from .models import Post, Profile
from .Serializer import Postserializer , ProfileSerializer


class PostList(generics.ListCreateAPIView):
    
    queryset = Post.objects.all()
    serializer_class = Postserializer
    
class PostDetail(generics.RetrieveAPIView):
    
    queryset = Post.objects.all()
    serializer_class = Postserializer



class UserList(generics.ListCreateAPIView):
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer