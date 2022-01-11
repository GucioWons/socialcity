import datetime

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils import timezone

from Accounts.models import Account, Notification, Request, Action, Comment, Post
from Accounts.forms import CommentForm


def profile_page(request, my_id):
    if not request.user.is_authenticated:
        return redirect('/landing')
    account = get_object_or_404(Account, id=my_id)
    user = account.user
    queryset = Post.objects.filter(user=user)
    context = {
        "object_list": queryset,
        "account": account,
        "user": user
    }
    return render(request, "profile_view.html", context)


# Dodawanie do znajomych
def add_to_friends(request, my_id):
    if not request.user.is_authenticated:
        return redirect('/landing')
    user = get_object_or_404(User, id=my_id)
    if not user.account.friends.all().contains(user):
        notification = Notification.objects.create(user=user)
        Request.objects.create(user=request.user, notification=notification)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_friends(request, my_id):
    if not request.user.is_authenticated:
        return redirect('/landing')
    user = get_object_or_404(User, id=my_id)
    friends_list = request.user.account.friends
    if friends_list.all().contains(user):
        friends_list.remove(user)
        user.account.friends.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def accept_request(request, my_id):
    if not request.user.is_authenticated:
        return redirect('/landing')
    notification = get_object_or_404(Notification, id=my_id)
    if notification.request:
        request.user.account.friends.add(notification.request.user)
        notification.request.user.account.friends.add(request.user)
        notification.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def decline_request(request, my_id):
    if not request.user.is_authenticated:
        return redirect('/landing')
    notification = get_object_or_404(Notification, id=my_id)
    if notification.request:
        notification.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#Like i Dislike
def like_view(request, my_id):
    if not request.user.is_authenticated:
        return redirect('/landing')
    post = get_object_or_404(Post, id=my_id)
    if not post.likes.all().contains(request.user):
        if post.dislikes.all().contains(request.user):
            post.dislikes.remove(request.user)
        post.likes.add(request.user)
        try:
            action = Action.objects.get(post=post, type='LIKE')
        except Action.DoesNotExist:
            action = None
        if not action:
            notification = Notification.objects.create(user=request.user)
            Action.objects.create(user=request.user, post=post, notification=notification, type='LIKE')
        else:
            action.user = request.user
            action.save()
            action.notification.save()
    else:
        post.likes.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def dislike_view(request, my_id):
    if not request.user.is_authenticated:
        return redirect('/landing')
    post = get_object_or_404(Post, id=my_id)
    if not post.dislikes.all().contains(request.user):
        if post.likes.all().contains(request.user):
            post.likes.remove(request.user)
        post.dislikes.add(request.user)
        try:
            action = Action.objects.get(post=post, type='DISLIKE')
        except Action.DoesNotExist:
            action = None
        if not action:
            notification = Notification.objects.create(user=request.user)
            Action.objects.create(user=request.user, post=post, notification=notification, type='DISLIKE')
        else:
            action.user = request.user
            action.save()
            action.notification.save()
    else:
        post.dislikes.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def post_view(request, my_id):
    if not request.user.is_authenticated:
        return redirect('/landing')
    post = get_object_or_404(Post, id=my_id)
    comments = Comment.objects.filter(post=post)
    form = CommentForm(request.POST or None, request.FILES)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.post = post
        new_comment.save()
        try:
            action = Action.objects.get(post=post, type='COMMENT')
        except Action.DoesNotExist:
            action = None
        if not action:
            notification = Notification.objects.create(user=request.user)
            Action.objects.create(user=request.user, post=post, notification=notification, type='COMMENT')
        else:
            action.user = request.user
            action.save()
            action.notification.save()
    context = {
        "form": form,
        "object": post,
        "queryset": comments
    }
    return render(request, "post_view.html", context)
