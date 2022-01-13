import datetime
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils import timezone

from Accounts.models import Account, Notification, Request, Action, Comment, Post
from Accounts.forms import CommentForm
from socialcity.settings import LOGS_ROOT


@login_required(login_url='/landing')
def profile_page(request, my_id):
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
@login_required(login_url='/landing')
def add_to_friends(request, my_id):
    user = get_object_or_404(User, id=my_id)
    if not user.account.friends.all().contains(user):
        notification = Notification.objects.create(user=user)
        Request.objects.create(user=request.user, notification=notification)
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n[" + timezone.now().strftime(
            "%Y-%m-%d %H:%M:%S") + "]: " + request.user.username + " wysłał zaproszenie do znajomych użytkownikowi " + user.username)
        f.close()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/landing')
def remove_from_friends(request, my_id):
    user = get_object_or_404(User, id=my_id)
    friends_list = request.user.account.friends
    if friends_list.all().contains(user):
        friends_list.remove(user)
        user.account.friends.remove(request.user)
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n[" + timezone.now().strftime(
            "%Y-%m-%d %H:%M:%S") + "]: " + request.user.username + " usunął ze znajomych użytkownika " + user.username)
        f.close()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/landing')
def accept_request(request, my_id):
    notification = get_object_or_404(Notification, id=my_id)
    if notification.request:
        request.user.account.friends.add(notification.request.user)
        notification.request.user.account.friends.add(request.user)
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n[" + timezone.now().strftime(
            "%Y-%m-%d %H:%M:%S") + "]: " + request.user.username + " zaakceptował prośbę użytkownika " + notification.request.user.username)
        f.close()
        notification.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/landing')
def decline_request(request, my_id):
    notification = get_object_or_404(Notification, id=my_id)
    if notification.request:
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n[" + timezone.now().strftime(
            "%Y-%m-%d %H:%M:%S") + "]: " + request.user.username + " odrzucił prośbę użytkownika " + notification.request.user.username)
        f.close()
        notification.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/landing')
def like_view(request, my_id):
    post = get_object_or_404(Post, id=my_id)
    if not post.likes.all().contains(request.user):
        if post.dislikes.all().contains(request.user):
            post.dislikes.remove(request.user)
        post.likes.add(request.user)
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n[" + timezone.now().strftime(
            "%Y-%m-%d %H:%M:%S") + "]: " + request.user.username + " lubi post o id = " + str(post.pk))
        f.close()
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


@login_required(login_url='/landing')
def dislike_view(request, my_id):
    post = get_object_or_404(Post, id=my_id)
    if not post.dislikes.all().contains(request.user):
        if post.likes.all().contains(request.user):
            post.likes.remove(request.user)
        post.dislikes.add(request.user)
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n[" + timezone.now().strftime(
            "%Y-%m-%d %H:%M:%S") + "]: " + request.user.username + " nie lubi posta o id = " + str(post.pk))
        f.close()
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


@login_required(login_url='/landing')
def post_view(request, my_id):
    post = get_object_or_404(Post, id=my_id)
    comments = Comment.objects.filter(post=post)
    form = CommentForm(request.POST or None, request.FILES)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.post = post
        new_comment.save()
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n[" + timezone.now().strftime(
            "%Y-%m-%d %H:%M:%S") + "]: " + request.user.username + " skomentował post o id = " + str(post.pk) + " (" + new_comment.content + ")")
        f.close()
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


@login_required(login_url='/landing/')
def delete_post_view(request, my_id):
    post = get_object_or_404(Post, id=my_id)
    if request.user == post.user:
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n[" + timezone.now().strftime(
            "%Y-%m-%d %H:%M:%S") + "]: " + request.user.username + " usunął post o treści (" + post.content + ") i id = " + str(post.pk))
        f.close()
        post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
