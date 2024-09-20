from rest_framework import generics,viewsets
from .models import Post, Profile
from .Serializer import Postserializer , ProfileSerializer


class PostViewsets(viewsets.ModelViewSet):
    
    queryset = Post.objects.all()
    serializer_class = Postserializer
    
# class PostDetail(generics.RetrieveAPIView):
    
#     queryset = Post.objects.all()
#     serializer_class = Postserializer



class UserViewsets(viewsets.ModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer