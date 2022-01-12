import os

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# Create your views here.
from django.utils import timezone

from Accounts.models import Account, Notification, Post
from Pages.forms import SignUpForm
from Accounts.forms import PostForm, UpdateTownForm, UpdateSchoolForm, UpdateImageForm, UpdateEmailForm, \
    UpdateLastNameForm, UpdateNameForm
from socialcity.settings import BASE_DIR, LOGS_ROOT


def home_page(request):
    if not request.user.is_authenticated:
        return redirect('/landing')
    form = PostForm(request.POST or None, request.FILES)
    friends = request.user.account.friends.all()
    queryset = Post.objects.all().order_by('-date')
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.user = request.user
        new_post.save()
        form = PostForm()
        f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
        f.write("\n[" + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + "]: " + request.user.username + " dodał post o tresci: (" + new_post.content + ") i id = " + str(new_post.pk))
        f.close()
    context = {
        "form": form,
        "queryset": queryset,
        "friends": friends
    }
    return render(request, "home_view.html", context)


def notification_page(request):
    if not request.user.is_authenticated:
        return redirect('/landing')
    queryset = Notification.objects.filter(user=request.user).order_by('-date')
    context = {
        "queryset": queryset
    }
    # Notification.objects.filter(user=request.user).update(new=False)
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
        f = open(os.path.join(LOGS_ROOT, user.username + "-logs.txt"), "a")
        f.write("\n[" + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + "]: " + user.username + "zarejestrował się w "
                                                                                               "serwisie")
        f.close()
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
                f = open(os.path.join(LOGS_ROOT, user.username + "-logs.txt"), "a")
                f.write("\n[" + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + "]: " + user.username + "zalogował się "
                                                                                                       "do serwisu")
                f.close()
                return redirect('pages:home-view')
        else:
            print()
    form = AuthenticationForm()
    return render(request, "login_view.html", context={"form": form})


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('/landing')
    logout(request)
    f = open(os.path.join(LOGS_ROOT, request.user.username + "-logs.txt"), "a")
    f.write("\n[" + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + "]: " + request.user.username + "wylogował się z serwisu")
    f.close()
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


def settings_page(request):
    if not request.user.is_authenticated:
        return redirect('/landing')
    form = UpdateNameForm(request.POST or None, instance=request.user)
    form2 = UpdateLastNameForm(request.POST or None, instance=request.user)
    form3 = UpdateEmailForm(request.POST or None, instance=request.user)
    form4 = UpdateImageForm(request.POST or None, request.FILES, instance=get_object_or_404(Account, user=request.user))
    form5 = UpdateSchoolForm(request.POST or None, instance=get_object_or_404(Account, user=request.user))
    form6 = UpdateTownForm(request.POST or None, instance=get_object_or_404(Account, user=request.user))
    if 'update_name' in request.POST:
        if form.is_valid():
            form.save()
    elif 'update_lastname' in request.POST:
        if form2.is_valid():
            form2.save()
    elif 'update_email' in request.POST:
        if form3.is_valid():
            form3.save()
    elif 'update_image' in request.POST:
        if form4.is_valid():
            form4.save()
    elif 'update_school' in request.POST:
        if form5.is_valid():
            form5.save()
    elif 'update_town' in request.POST:
        if form6.is_valid():
            form6.save()
    return render(request, "settings_view.html", context={'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6, })
