from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.


def shibboleth_test(request: HttpRequest):
    meta = request.META
    
    s = '<pre>\n'
    for k, v in meta.items():
        s += k + ': ' + str(v) + '\n'
    s += '</pre>\n'

    return HttpResponse(s)
