from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from time import mktime

from .models import Request

def index(request):
  return render(request, 'fuse/index.html', {'requests': Request.objects.all()})

def submit(request):
  redirect_script = '<script type="text/javascript">setTimeout(function(){window.location.replace('+reverse('fuse:index')+');}, 2000);</script>'
  try:
    if request.POST['pass'] == "RaspberryStart":
      Request().save()
      return redirect('fuse:index')
    else:
      return HttpResponse("Incorrect Parrword!"+redirect_script)
  except (KeyError):
    return HttpResponse("You need to submit a password!"+redirect_script)

def check(request):
  if len(Request.objects.filter(recieved=False)):
    r = Request.objects.filter(recieved=False).order_by('-request_time')[0]
  else:
    return JsonResponse({'signal': False})
  if request.GET.get('dismiss'):
    r.recieved = True
    r.save()
  return JsonResponse({'signal': True, 'timestamp': mktime(r.request_time.timetuple())})

def verify(request):
  return HttpResponse("Hello, world!")
