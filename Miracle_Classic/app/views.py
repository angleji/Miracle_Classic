from django.shortcuts import render, redirect
from .models import Book, Post, Comment, Recomment, Like, Scrap
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json



# Create your views here.
def home(request):
    posts = sorted(Post.objects.all(), key=lambda x: -x.comments_count())
    books = Book.objects.all()

    return render(request, 'home.html', {'hot_posts':posts[:2], 'books': books})


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {"books":books})

def book_detail(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    return render(request, 'book_detail.html', {"book":book})

@login_required(login_url='/registration/login')
def post_add(request, book_pk):
    if request.method == 'POST':
        new_post = Post.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            book=Book.objects.get(pk=book_pk),
            user=User.objects.get(username=request.user)
        )
        return redirect('post_detail', new_post.pk)

    return render(request, 'post_add.html')


@csrf_exempt
@login_required(login_url='/registration/login')
def book_scrap(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        book=Book.objects.get(pk=request_body['book_pk'])
        scrap, add_scrap = Scrap.objects.get_or_create(
            book=book,
            user=User.objects.get(username=request.user)
        )

        if not add_scrap:
            scrap.delete()

        scraps_count = Scrap.objects.filter(book=book).count()

        return HttpResponse(json.dumps({'is_scrap':add_scrap, 'scraps_count':scraps_count}))


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts':posts})

def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    return render(request, 'post_detail.html', {'post':post})


@login_required(login_url='/registration/login')
def post_edit(request, post_pk):
    post = Post.objects.filter(pk=post_pk)
    if request.method == 'POST':
        post.update(
            title=request.POST['title'],
            content=request.POST['content']
        )
        
        return redirect('post_detail', post_pk)

    return render(request, 'post_edit.html', {'post':post[0]})


@login_required(login_url='/registration/login')
def post_delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    book_pk = post.book.pk
    post.delete()

    return redirect('book_detail', book_pk)


@csrf_exempt
@login_required(login_url='/registration/login')
def post_like(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        print(request_body)
        post=Post.objects.get(pk=request_body['post_pk'])
        like, add_like = Like.objects.get_or_create(
            post=post,
            user=User.objects.get(username=request.user)
        )

        if not add_like:
            like.delete()

        likes = Like.objects.filter(post=post)
        
        return HttpResponse(json.dumps({'is_like':add_like, 'likes_count':likes.count()}))

            

@login_required(login_url='/registration/login')
def comment_add(request, post_pk):
    if request.method == 'POST':
        new_comment = Comment.objects.create(
            post=Post.objects.get(pk=post_pk),
            user=User.objects.get(username=request.user),
            content=request.POST['content']
        )
        return redirect('post_detail', post_pk)


@login_required(login_url='/registration/login')
def comment_delete(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    post_pk = comment.post.pk
    comment.delete()

    return redirect('post_detail', post_pk)


@login_required(login_url='/registration/login')
def recomment_add(request, post_pk, comment_pk):
    if request.method == 'POST':
        post=Post.objects.get(pk=post_pk)
        comment=Comment.objects.get(pk=comment_pk)
        
        new_recomment = Recomment.objects.create(
            post=post,
            comment=comment,
            user=User.objects.get(username=request.user),
            content=request.POST['content']
        )

        return redirect('post_detail', post.pk)
    

@login_required(login_url='/registration/login')
def recomment_delete(request, recomment_pk):
    recomment = Recomment.objects.get(pk=recomment_pk)
    post_pk = recomment.post.pk
    recomment.delete()

    return redirect('post_detail', post_pk)


def signup(request):
    if request.method == 'POST':
        user, new = User.objects.get_or_create(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )

        if new:
            auth.login(request, user)
            return redirect('home')
    return render(request, 'signup.html')


@csrf_exempt
def check_exists(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        email = request_body['email']
        username = request_body['username']
        print(email)
        exists = True
        
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                exists = False

        elif username:
            try:
                user = User.objects.get(username=username)
                print(user)
            except User.DoesNotExist:
                exists = False

        response = {'exists':exists}
        return HttpResponse(json.dumps(response))


@csrf_exempt
def login(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        email = request_body['email']
        password = request_body['password']

        response = {
            'state' : True,
        }
        
        try:
            user = User.objects.get(email=email, password=password)
            auth.login(request, user)
        except User.DoesNotExist:
            response['state'] = False
        
        return HttpResponse(json.dumps(response))

    return render(request, 'login.html')
    

@login_required(login_url='/registration/login')
def logout(request):
    auth.logout(request)

    return redirect('home')

@login_required(login_url='/registration/login')
def signout(request):
    user = User.objects.get(username=request.user)
    user.delete()
    
    return redirect('home')



def user_profile(request, username):
    user = User.objects.get(username=username)
    scraps = set()
    for e in Scrap.objects.select_related('user'):
        scraps.add(e.book)

    posts = Post.objects.filter(user=user)
    liked_posts = set()
    # 더 알아보기. join이 django에서 어떻게 일어나는거지?
    for e in Like.objects.select_related('user'):
        liked_posts.add(e.post)

    comment = username + "의 서재입니다"
    if username == request.user.username:
        comment = "안녕하세요 " + username + " 님"

    return render(request, 'user_profile.html', {'scraps':scraps, 'posts':posts, 'liked_posts':liked_posts, 'comment':comment})

