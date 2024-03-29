from django.shortcuts import redirect
from django.urls import Resolver404, resolve


def next_redirect(default_path="uts_common:index", allow_external_redirects=False):
    def wrapper(fn):
        def inner(request, *args, **kwargs):
            result = fn(request, *args, **kwargs)
            if result is not None:
                return result
            if "next" in request.GET:
                if allow_external_redirects:
                    return redirect(request.GET["next"])
                return redirect(f"{request.scheme}://{request.get_host()}{request.GET['next']}")
            return redirect(default_path)
        return inner
    return wrapper
