from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q

# Create your views here.
from Accounts.models import Account, Notification, Post
from Pages.forms import SignUpForm
from Accounts.forms import PostForm


def home_page(request):
    if not request.user.is_authenticated:
        return redirect('/landing')
    form = PostForm(request.POST or None, request.FILES)
    queryset = Post.objects.all().order_by('-date')
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.user = request.user
        new_post.save()
    context = {
        "form": form,
        "queryset": queryset
    }
    return render(request, "home_view.html", context)


def notification_page(request):
    if not request.user.is_authenticated:
        return redirect('/landing')
    queryset = Notification.objects.filter(user=request.user).order_by('-date')
    context = {
        "queryset": queryset
    }
    #Notification.objects.filter(user=request.user).update(new=False)
    return render(request, "notification_view.html", context)

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, "landing_view.html", context={})


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Account.objects.create(user=user)
        login(request, user)
        return redirect("pages:home-view")
    context = {
        "form": form
    }
    return render(request, "register_view.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pages:home-view')
            else:
                print()
        else:
            print()
    form = AuthenticationForm()
    return render(request, "login_view.html", context={"form": form})


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('/landing')
    logout(request)
    return redirect("pages:landing-view")


def search_page(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('/landing')
    query = request.GET.get('query')
    users_list = User.objects.filter(
        (Q(first_name__icontains=query) | Q(last_name__icontains=query))
    )
    context = {
        "queryset": users_list
    }
    return render(request, "search_view.html", context)
