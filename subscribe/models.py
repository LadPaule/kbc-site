from django.db import models 
class Subscriber(models.Model):
  email = models.EmailField(unique=True) 
  conf_num = models.CharField(max_length=15) 
  confirmed = models.BooleanField(default=False) 
  def __str__(self):
    return self.email + " (" + ("not " if not         self.confirmed else "") + "confirmed)"