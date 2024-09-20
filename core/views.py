from itertools import chain
from django.shortcuts import render , redirect
from django.contrib.auth.models import User 
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile,Post,LikePost , FollowersCount
import random

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user)
    profile_object = Profile.objects.get(user=user_object)
    
    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
        
    feed_list = list(chain(*feed))
    
    # add suggestions
    all_users = User.objects.all()
    user_following_all = []
    
    for user in user_following:
        user_list = User.objects.get(username=user.user) 
        user_following_all.append(user_list)
        
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username) 
    finale_suggestions_all = [x for x in list(new_suggestions_list) if (x not in list(current_user))]   

    random.shuffle(finale_suggestions_all)
    
    username_profile = []
    username_profile_list = []

    for users in finale_suggestions_all:
        username_profile.append(users.id)
    
    for ids in username_profile:
        profile_lists = Profile.objects.filter(user__id=ids)
        username_profile_list.append(profile_lists)
    
    # Always define suggestions_username_profile_list, even if the loop doesn't run
    suggestions_username_profile_list = []
    
    if username_profile_list:
        suggestions_username_profile_list = list(chain(*username_profile_list))
    
    return render(request, 'index.html', {
        "profile_object": profile_object, 
        "posts": feed_list, 
        'suggestions_username_profile_list': suggestions_username_profile_list[:4]
    })



def search(request):
    
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)
        
        
        
        username_profile = []
        username_profile_list = []
        
        for users in username_object:
            username_profile.append(users.id)
            
            
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        
        username_profile_list = list(chain(*username_profile_list))
            
    return render(request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})

def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES['image_upload']
        caption =request.POST['caption']
        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    
    else:
        return redirect('/')



@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id,username=username).first()
    if like_filter == None :
        new_like = LikePost.objects.create(post_id = post_id,username = username)
        new_like.save()
        post.no_of_likes =post.no_of_likes+1
        post.save()
        print(f'total post numper {post.no_of_likes}')
        return redirect('/')
    
    else:
        like_filter.delete()
        post.no_of_likes =post.no_of_likes - 1
        post.save()
        return redirect('/')


@login_required(login_url='signin')
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    follower = request.user.username
    user=pk
    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'follow'
        
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'button_text':button_text,
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_followers':user_followers,
        'user_following':user_following,
    }
    return render(request,'profile.html',context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower,user=user):
            delete_follower= FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follow = FollowersCount.objects.create(follower=follower,user=user)
            new_follow.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
        
@login_required(login_url='signin')
def settings(request):
    user_porfile = Profile.objects.get(user=request.user)

    if request.method == 'POST':


        if request.FILES.get('image')==None :
            image= user_porfile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            user_porfile.profileimg = image
            user_porfile.bio = bio
            user_porfile.location = location
            user_porfile.save()
        
        if request.FILES.get('image')!=None :
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_porfile.bio = bio
            user_porfile.location = location
            user_porfile.profileimg = image
            user_porfile.save()


        return redirect('settings')
    return render(request,'setting.html',{'user_profile':user_porfile})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2 :
            # if User.objects.filter(email=email).exists():
            #     messages.info(request,'Email Taken')
            #     return redirect('signup')
            
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user (username=username,email=email,password=password)
                user.save()
                
              

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()


                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                return redirect('settings')
        else :
            messages.info(request,'Password Not Matching')
            return redirect('signup')
    else :

        return render(request,'signup.html')
    

def signin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credential Invalid ')
            return redirect('/signin')
    else:
        return render(request,'signin.html')
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


