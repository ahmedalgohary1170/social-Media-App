from rest_framework import generics
from .models import Post
from .Serializer import Postserializer


class PostList(generics.ListCreateAPIView):
    
    queryset = Post.objects.all()
    serializer_class = Postserializer
    
class PostDetail(generics.RetrieveAPIView):
    
    queryset = Post.objects.all()
    serializer_class = Postserializer
