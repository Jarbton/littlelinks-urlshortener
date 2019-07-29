from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template.context_processors import csrf
from urllib.parse import urlparse
from .forms import UrlForm
import random, string, json, requests, re

from littlelinksite.models import Shorturl


def index(request):
    form = UrlForm(request.POST or None)

    context = {
        'form' : form
    }

    if form.is_valid():
        new_url_id = get_new_url()
        url = form.cleaned_data['orig_url']
        b = Shorturl(orig_url=url, new_url_id=new_url_id)
        b.save()

        output_url = settings.SITE_URL + "/" + new_url_id

        context["littlelink"] = output_url

    return render(request, "littlelinksite/index.html", context)

def redirect_original(request, new_url_id):
    url = get_object_or_404(Shorturl, pk=new_url_id)
    url.no_clicks += 1
    url.save()
    return HttpResponseRedirect(url.orig_url)

def shorten_url(request):
    url = request.POST.get("url", '')
    if not (url == ''):
        if check_url(url):
            new_url_id = get_new_url()
            b = Shorturl(orig_url=url, new_url_id=new_url_id)
            b.save()

            response_data = {}
            response_data['url'] = settings.SITE_URL + "/" + new_url_id
            return HttpResponse(json.dumps(response_data), content_type="application/json")  
    return HttpResponse(json.dumps({"error": "error occurs"}), content_type="application/json")

def get_new_url():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        new_url_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Shorturl.objects.get(pk=new_url_id)
        except:
            return new_url_id

# Get new URL for three word address
# def get_new_url():
#     length = 3
#     # word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
#     # response = requests.get(word_site)
#     # words = response.content.splitlines()
#     # words = str(words)
#     words = ("rsk", "orbital", "tesla", "space", "mickey")

#     while True:
#         new_url_id = ''.join(random.choice(words) for x in range(length))
#         try:
#             temp = Shorturl.objects.get(pk=new_url_id)
#         except:
#             return new_url_id