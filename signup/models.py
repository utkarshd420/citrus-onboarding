from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
# Create your models here.
class new(models.Model):
  user = models.OneToOneField(User)
  company_name = models.CharField(max_length=100)
  company_category = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  phone = models.CharField(max_length=15)
  reg_date = models.CharField(max_length=30)
  step = models.IntegerField(default=1)
  def __unicode__(self):
    return self.company_name
def create_user_profile(sender, instance, created, **kwargs):  
  if created:  
     profile, created = new.objects.get_or_create(user=instance)  
post_save.connect(create_user_profile, sender=User)   
