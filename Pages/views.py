from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

# Create your views here.
from Pages.forms import SignUpForm
from Posts.forms import PostForm
from Posts.models import Post


def home_page(request):
    if not request.user.is_authenticated:
        return redirect('/landing')
    form = PostForm(request.POST or None, request.FILES)
    queryset = Post.objects.all().order_by('-date')
    if form.is_valid():
        new_post=form.save(commit=False)
        new_post.user=request.user
        new_post.save()
    context = {
        "form": form,
        "queryset": queryset
    }
    return render(request, "home_view.html", context)


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
        login(request, user)
        return redirect("home-page")
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
                return redirect('/')
            else:
                print()
        else:
            print()
    form = AuthenticationForm()
    return render(request, "login_view.html", context={"form": form})
