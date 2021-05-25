from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout, authenticate, login
from django_q.tasks import schedule

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
def organizations_list(request):
    return render(request, "uts/organizations-list.html")


@login_required
def new_ticket_form(request):
    if request.POST:
        form = TicketForm(request.POST, user=request.user)
        if form.is_valid():
            owner_id = int(form.cleaned_data["owner"])
            name = form.cleaned_data["name"]
            tags = form.cleaned_data["tags"]
            scheduled = form.cleaned_data["scheduled"]
            if scheduled:
                scheduled_datetime = form.cleaned_data["scheduled_datetime"]
                schedule('uts_scheduler.schedules.new_ticket',
                         request.user.id, owner_id, name, tags=tags,
                         next_run=scheduled_datetime,
                         schedule_type='O')
                return render(request, "uts/new-ticket.html", context={"scheduleSuccess": True, "form": TicketForm(user=request.user)})
            ticket_id = Ticket.create(request.user.id, owner_id, name, tags)
            return redirect("uts_common:ticket_details", ticket_id)
    else:
        form = TicketForm(user=request.user)
    return render(request, "uts/new-ticket.html", context={"form": form})


@login_required
def profile_settings_form(request):
    if request.POST:
        form = ProfileSettingsForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
        return render(request, "uts/profile-settings.html", context={"saveSuccess": True, "form": ProfileSettingsForm(instance=request.user.profile)})
    form = ProfileSettingsForm(instance=request.user.profile)
    return render(request, "uts/profile-settings.html", context={"form": form})
