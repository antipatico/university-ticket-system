from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

from uts_common.decorators import next_redirect


def index(request):
    if request.user.is_authenticated:
        return render(request, "uts/index.html")
    return render(request, "uts/welcome.html")


@next_redirect()
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)


def local_login(request):
    return render(request, "uts/local-login.html")