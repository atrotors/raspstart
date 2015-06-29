from django.db import models
from time import mktime

class Request(models.Model):
  recieved = models.BooleanField(default=False)
  request_time = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return str(self.recieved) + ', ' + str(self.request_time)
