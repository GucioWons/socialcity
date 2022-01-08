from django.contrib.auth.models import User
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
