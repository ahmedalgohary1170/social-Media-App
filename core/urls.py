from django.urls import path
from . import views , api

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings,name='settings'),
    path('upload', views.upload,name='upload'),
    path('search', views.search,name='search'),
    path('follow', views.follow,name='follow'),
    path('profile/<str:pk>', views.profile,name='profile'),
    path('like-post',views.like_post,name='like-post'),
    path('signup', views.signup,name='signup'),
    path('signin', views.signin,name='signin'),
    path('logout', views.logout,name='logout'),
    
    # api
    path('api/posts',api.PostList.as_view()),
    path('api/posts/<str:pk>',api.PostDetail.as_view())

]
