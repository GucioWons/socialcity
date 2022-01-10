from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from Accounts.models import Account
from Posts.models import Post


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

def add_to_friends(request, my_id):
    if not request.user.is_authenticated:
        return redirect('/landing')
    user = get_object_or_404(User, id=my_id)
    friends_list = request.user.account.friends
    print(user)
    if not friends_list.all().contains(user):
        friends_list.add(user)
        user.account.friends.add(request.user)
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