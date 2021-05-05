from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, authenticate, login

from uts_common.decorators import next_redirect
from uts_common.forms import *
from uts_common.models import Ticket


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
