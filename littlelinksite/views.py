from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template.context_processors import csrf
from django.views import View
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from urllib.parse import urlparse
from .forms import UrlForm

import urllib.request
import random, string, json, re

from littlelinksite.models import Shorturl



class IndexView(View):
    template_name = 'littlelinksite/index.html'
    form_class = UrlForm

    def get(self, request):
        form = self.form_class

        context = {'form' : form}

        return render(request, self.template_name, context)
    
    def post(self, request):
        form_class = self.form_class
        form = form_class(request.POST)

        context = { 'form' : form }

        if form.is_valid():
            # Check if user requested three word url
            word_url_bool = form.cleaned_data['word_url_bool']
            if word_url_bool:
                new_url_id = get_new_word_url()
            else:
                new_url_id = get_new_url()

            url = form.cleaned_data['orig_url']

            # If user is auth. add to URL in DB
            if request.user.is_authenticated:
                user = request.user
                b = Shorturl(orig_url=url, new_url_id=new_url_id, user=user)
            else:
                b = Shorturl(orig_url=url, new_url_id=new_url_id)
            b.save()

            output_url = settings.SITE_URL + "/" + new_url_id
            context["littlelink"] = output_url

        return render(request, self.template_name, context)


class LinksView(View):
    template_name = 'littlelinksite/mylittlelinks.html'

    def get(self, request):
        if not request.user.is_authenticated:
            # TODO: Add redirect with the intention to load mylittlelinks
            # Context?
            return HttpResponseRedirect('accounts/login')
        
        # Get user and query for URLS
        user = request.user
        s = Shorturl.objects.all().filter(user=user)

        # Set context to result
        context = {'shorturl_list' : s}

        return render(request, self.template_name, context)


class DeleteURLView(UserPassesTestMixin, DeleteView):
    template_name = 'littlelinksite/url_delete.html'
    raise_exception = True

    def test_func(self):
        self.object = self.get_object() 
        return self.object.user == self.request.user

    def get_object(self):
        url_id = self.kwargs.get("new_url_id")
        print(url_id)
        return get_object_or_404(Shorturl, pk=url_id)

    def get_success_url(self):
        return reverse('mylittlelinks')


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def redirect_original(request, new_url_id):
    url = get_object_or_404(Shorturl, pk=new_url_id)
    url.no_clicks += 1
    url.save()
    return HttpResponseRedirect(url.orig_url)


def get_new_url():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        new_url_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Shorturl.objects.get(pk=new_url_id)
        except:
            return new_url_id


def get_new_word_url():
    length = 3
    word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = urllib.request.urlopen(word_url)
    long_txt = response.read().decode()
    words = long_txt.splitlines()

    # words = ("rsk", "orbital", "tesla", "space", "mickey")

    new_url_id = ''
    while True:
        for x in range(length):
            new_url_id = new_url_id + random.choice(words)
            if x < length - 1:
                new_url_id = new_url_id + "-"
        try:
            temp = Shorturl.objects.get(pk=new_url_id)
        except:
            return new_url_id


# def index(request):
#     form = UrlForm(request.POST or None)

#     context = {
#         'form' : form
#     }

#     if form.is_valid():
#         new_url_id = get_new_url()
#         url = form.cleaned_data['orig_url']
#         b = Shorturl(orig_url=url, new_url_id=new_url_id)
#         b.save()

#         output_url = settings.SITE_URL + "/" + new_url_id

#         context["littlelink"] = output_url

#     return render(request, "littlelinksite/index.html", context)
