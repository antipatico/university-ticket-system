from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from uts_common.models import User
from django.shortcuts import render


def shibboleth_login(request: HttpRequest):
    meta = request.META
    user, created = User.objects.get_or_create(username=meta["HTTP_EPPN"])
    if created:
        user.set_unusable_password()
        if "HTTP_MAIL" in meta:
            user.email = f"{meta['HTTP_MAIL']}"
        if "HTTP_GIVENNAME" in meta:
            user.first_name = f"{meta['HTTP_GIVENNAME']}".capitalize()
        if "HTTP_SN" in meta:
            user.last_name = f"{meta['HTTP_SN']}".capitalize()

    user.save()
    login(request, user)
    return HttpResponseRedirect("/")


def shibboleth_test(request: HttpRequest):
    meta = request.META
    
    s = '<pre>\n'
    for k, v in meta.items():
        s += k + ': ' + str(v) + '\n'
    s += '</pre>\n'

    return HttpResponse(s)
