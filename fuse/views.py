from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime
import redis

from .models import Request

def index(request):
  alert = {'exist': False, 'label': None, 'text': None}

  if 'a' in request.GET and request.GET['a'] in ['wrong', 'nopass', 'pass']:
    alert['exist'] = True

    if request.GET['a'] == 'wrong':
      alert['label'] = 'warning'
      alert['text'] = 'Wrong password, try again!'

    elif request.GET['a'] == 'nopass':
      alert['label'] = 'danger'
      alert['text'] = 'You have to enter the password!'

    else:
      alert['label'] = 'success'
      alert['text'] = 'Request sent.'

  return render(request, 'fuse/index.html', {
      'requests': Request.objects.all(),
      'alert': alert
    })

def submit(request):
  try:
    if request.POST['pass'] == 'RaspberryStart':
      Request().save()
      return HttpResponseRedirect(reverse('fuse:index') + '?a=pass')

    else:
      return HttpResponseRedirect(reverse('fuse:index') + '?a=wrong')

  except (KeyError):
    return HttpResponseRedirect(reverse('fuse:index') + '?a=nopass')

def check(request):
  if len(Request.objects.filter(recieved=False)):
    r = Request.objects.filter(recieved=False).order_by('-request_time')[0]

  else:
    return JsonResponse({'signal': False})

  if request.GET.get('dismiss'):
    r.recieved = True
    r.save()

    red = redis.StrictRedis(host='localhost', port=6379, db=0)
    red.publish('fuse.socketio', r.id)

  return JsonResponse({'signal': True, 'timestamp': r.get_timestamp()})
