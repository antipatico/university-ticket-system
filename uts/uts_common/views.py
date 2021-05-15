from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout, authenticate, login
from uts_common.decorators import next_redirect
from uts_common.forms import *
from uts_common.models import *


def index(request):
    if request.user.is_authenticated:
        return render(request, "uts/index.html")
    return render(request, "uts/welcome.html")


@next_redirect()
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)


@next_redirect()
def local_login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.data["username"], password=form.data["password"])
            if user is not None:
                login(request, user)
                return  # Redirect to index thanks to next_redirect decorator
            form.add_error(None, "Username o password non validi")
    else:
        form = LoginForm()
    return render(request, "uts/local-login.html", context={"form": form})


@login_required
def ticket_details(request, pk):
    if not Ticket.objects.filter(pk=pk).exists():
        raise Http404
    return render(request, "uts/ticket-details.html", context={"ticket_id": pk})


@login_required
@transaction.atomic
def new_ticket_form(request):
    if request.POST:
        form = TicketForm(request.POST, user=request.user)
        if form.is_valid():
            owner = get_object_or_404(Owner.objects.all(), pk=int(form.cleaned_data["owner"]))
            """
            # The following checks are not needed since django's form will check for the choices on post.
            if type(owner) is Individual and owner.id != request.user.individual.id:
                form.add_error("owner", "Non puoi creare un ticket come qualcun altro")
            elif owner.admin.id != request.user.id and request.user not in owner.members:
                form.add_error("owner", "Non puoi creare un ticket per un organizzazione di cui non fai parte")
            """
            name = form.cleaned_data["name"]
            tags = [Tag.objects.get_or_create(tag=tag)[0] for tag in form.cleaned_data["tags"]]
            ticket = Ticket.objects.create(owner=owner, name=name)
            ticket.tags.set(tags)
            ticket.save()
            event = TicketEvent.objects.create(ticket=ticket, owner=request.user.individual, status=TicketStatus.OPEN)
            event.save()
            if type(owner) is Organization:
                ticket.subscribers.set(owner.members.all())
                ticket.subscribers.add(owner.admin)

            return redirect("uts_common:ticket_details", ticket.id)
    else:
        form = TicketForm(user=request.user)
    return render(request, "uts/new-ticket.html", context={"form": form})
