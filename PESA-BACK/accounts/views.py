'''pesapot views'''
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import logout
from remitapi.decorators import logged_out_required
from accounts.forms import CustomRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from registration.backends.default.views import RegistrationView
from registration import signals
from registration.users import UserModel


def render_view(request, template, data):
    '''
    wrapper for rendering views , loads RequestContext
    @request  request object
    @template  string
    @data  tumple
    '''
    template = 'accounts/%s' % template
    data['STATIC_URL'] = '%sdashboard/' % settings.STATIC_URL
    return render_to_response(
        template, data,
        context_instance=RequestContext(request)
    )


@logged_out_required
def user_login(request):
    '''
    handles the index page when user is not logged in
    @request  request object
    '''
    form = AuthenticationForm()
    if request.POST:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Okay, security check complete. Log the user in.
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('home'))
    return render_view(request, 'login.html', {'form': form})


@logged_out_required
def signup(request):
    '''
    handles the index page when user is not logged in
    @request  request object
    '''
    form = CustomRegistrationForm()
    if request.POST:
        data = request.POST.copy()
        data['username'] = data.get('email', None)
        form = CustomRegistrationForm(data)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username, email, password = cleaned_data[
                'username'], cleaned_data['email'], cleaned_data['password1']
            new_user = UserModel().objects.create_user(
                username, email, password)
            new_user.is_active = True
            new_user.save()
            signals.user_registered.send(sender=RegistrationView,
                                         user=new_user,
                                         request=request
                                         )
            login(request, new_user)
            return HttpResponseRedirect(reverse('home'))
        else:
            print form.errors
    return render_view(request, 'signup.html',
                       {'form': form}
                       )


def signout(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse('landing_page'))
