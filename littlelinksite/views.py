from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template.context_processors import csrf
from django.views import View
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
            word_url_bool = form.cleaned_data['word_url_bool']
            if word_url_bool:
                new_url_id = get_new_word_url()
            else:
                new_url_id = get_new_url()

            url = form.cleaned_data['orig_url']
            b = Shorturl(orig_url=url, new_url_id=new_url_id)
            b.save()

            output_url = settings.SITE_URL + "/" + new_url_id

            context["littlelink"] = output_url

        return render(request, self.template_name, context)


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
