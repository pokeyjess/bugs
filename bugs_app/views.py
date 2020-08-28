from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from bugs_app.models import MyUser, Ticket
from bugs_app.forms import CustomUserForm, LoginForm, TicketForm

def index(request):
    tickets = Ticket.objects.all().order_by('-time_created')
    users = MyUser.objects.all().order_by('-display_name')
    return render(request, 'index.html', {"tickets": tickets, "users": users})

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
    else:
        return HttpResponseForbidden("Non-staff not allowed")


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

def ticket_form_view(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(title=data.get('title'), description=data.get('description'), creator=request.user, status='N')
            return HttpResponseRedirect(reverse("homepage"))
    form = TicketForm()
    return render(request, "generic_form.html", {"form": form})

def ticket_detail_view(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, "ticket_detail.html", {"ticket": ticket})

def user_detail_view(request, user_id):
    user = MyUser.objects.filter(id=user_id).first()
    ticket_list = Ticket.objects.filter(owner=user)
    return render(request, "user_detail.html", {"user": user, "tickets": ticket_list})