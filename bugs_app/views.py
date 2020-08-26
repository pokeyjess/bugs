from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from bugs_app.models import MyUser
from bugs_app.forms import CustomUserForm, LoginForm

def index(request):
    return render(request, 'index.html')

@login_required
def signup_view(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = CustomUserForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                MyUser.objects.create_user(username=data.get("username"), password=data.get("password"), display_name=data.get("display_name"))
                return HttpResponseRedirect(reverse("homepage"))
        
        form = CustomUserForm()
        return render(request, "generic_form.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


