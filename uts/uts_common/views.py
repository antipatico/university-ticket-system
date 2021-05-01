from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.urls import resolve, Resolver404

from uts_common.decorators import next_redirect


def index(request):
    return render(request, "uts/index.html")


@next_redirect()
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
