'''Decorators'''
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse


def logged_out_required(function):
    '''This page cannot be viewed if a user is logged'''
    def wrapper(request, *args, **kw):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return function(request, *args, **kw)
    return wrapper


def fixer_required(function):
    '''This page cannot be viewed if a user is logged out '''
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('404'))
        else:
            if not request.user.is_superuser and not request.user.is_superuser:
                return HttpResponseRedirect(reverse('404'))
            return function(request, *args, **kw)
    return wrapper


def login_required(function):
    '''This page cannot be viewed if a user is logged out '''
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        else:
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse('backend'))
            else:
                return function(request, *args, **kw)
    return wrapper


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            # return HttpResponseBadRequest()
            return HttpResponseRedirect(reverse('404'))
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
