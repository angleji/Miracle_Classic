"""Miracle_Classic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # 메인 페이지
    path('', home, name='home'),

    # 도서
    path('book_list', book_list, name='book_list'),
    path('book_detail/<int:book_pk>', book_detail, name='book_detail'),

    # 도서 저장 / 글쓰기
    path('post_add/<int:book_pk>', post_add, name='post_add'),
    path('book_scrap', book_scrap, name='book_scrap'),

    # 토론글
    path('post_list', post_list, name='post_list'),
    path('post_detail/<int:post_pk>', post_detail, name='post_detail'),
    path('post_edit/<int:post_pk>', post_edit, name='post_edit'),
    path('post_delete/<int:post_pk>', post_delete, name='post_delete'),

    # 토론글 좋아요
    path('post_like', post_like, name='post_like'),

    # 댓글
    path('comment_add/<int:post_pk>', comment_add, name='comment_add'),
    path('comment_delete/<int:comment_pk>', comment_delete, name='comment_delete'),

    # 답글
    path('recomment_add/<int:post_pk>/<int:comment_pk>', recomment_add, name='recomment_add'),
    path('recomment_delete/<int:recomment_pk>', recomment_delete, name='recomment_delete'),

    # 회원관리
    path('registration/login', login, name='registration/login'),
    path('registration/logout', logout, name='registration/logout'),
    path('registration/signup', signup, name='registration/signup'),
    path('registration/signup/check_exists', check_exists, name='registration/signup/check_exists'),
    path('registration/signout', signout, name='registration/signout'),

    # 사용자 프로필
    path('user_profile/<str:username>', user_profile, name='user_profile')

]
