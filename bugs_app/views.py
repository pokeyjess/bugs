from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from bugs_app.models import MyUser, Ticket
from bugs_app.forms import CustomUserForm, LoginForm, TicketForm

@login_required
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

@login_required
def ticket_form_view(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(title=data.get('title'), description=data.get('description'), creator=request.user, status='N')
            return HttpResponseRedirect(reverse("homepage"))
    form = TicketForm()
    return render(request, "generic_form.html", {"form": form})

@login_required
def ticket_detail_view(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, "ticket_detail.html", {"ticket": ticket})

@login_required
def user_detail_view(request, user_id):
    user = MyUser.objects.filter(id=user_id).first()
    ticket_created = Ticket.objects.filter(creator=user)
    ticket_working = Ticket.objects.filter(owner=user)
    ticket_completed = Ticket.objects.filter(last_owner=user)
    return render(request, "user_detail.html", {"user": user, "ticket_created": ticket_created, "ticket_working": ticket_working, "ticket_completed": ticket_completed})

@login_required
def ticket_edit_view(request, id):
    edit = get_object_or_404(Ticket, id=id)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=edit)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.save()
            return redirect('ticket', edit.pk)
    else:
        form = TicketForm(instance=edit)
    return render(request, 'generic_form.html', {'form': form})

# https://tutorial.djangogirls.org/en/django_forms/
# https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/


@login_required
def assign_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.status = "P"
    ticket.owner = request.user
    ticket.save()
    return redirect('ticket', ticket.pk)

@login_required
def invalid_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.status = "I"
    ticket.owner = None
    ticket.save()
    return redirect('ticket', ticket_id)

@login_required
def finished_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.status = "D"
    ticket.owner = None
    ticket.last_owner = request.user
    ticket.save()
    return redirect('ticket', ticket_id)

@login_required
def reopen_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.status ="N"
    ticket.creator = request.user
    ticket.owner = None
    ticket.last_owner = None
    ticket.save()
    return redirect('ticket', ticket_id)


