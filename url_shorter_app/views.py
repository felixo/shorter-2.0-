from django.shortcuts import render, get_object_or_404, redirect
import random, string, json, hashlib, logging
from url_shorter_app.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template.context_processors import csrf


def index(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'url_shorter_app/index.html', c)


def redirect_original(request, short_id):
    url = get_object_or_404(Urls, pk=short_id)  # get object, if not        found return 404 error
    url.count += 1
    url.save()
    logging.warning('URL IS: ' + url.httpurl)
    return redirect(url.httpurl)


def shorten_url(request):
    url = request.POST.get("url", '')
    if url:
        short_id = get_short_code(url)
        b = Urls(httpurl=url, short_id=short_id)
        b.save()
        response_data = {}
        response_data['url'] = settings.SITE_URL + "/" + short_id
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponse(json.dumps({"Error": "Sorry, We can't get your URL"}), content_type="application/json")


def get_short_code(url):
    while True:
        short_id = ''.join(hashlib.md5(url.encode('utf-8')).hexdigest()[:settings.LENGTH])
        try:
            temp = Urls.objects.get(pk=short_id)
        except:
            logging.warning(short_id)
            return short_id
