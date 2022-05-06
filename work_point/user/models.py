from django.db import models
from client.models import User as ClientUser
# Create your models here.




class UserQualification(models.Model):
    user = models.ForeignKey(ClientUser,on_delete=models.CASCADE)
    recent_degree = models.CharField(max_length=30)
    cpi = models.PositiveIntegerField()
    passing_year = models.PositiveIntegerField()
    university = models.CharField(max_length=30)
    about  =  models.CharField(max_length=200)

   

class UserExperience(models.Model):
    user = models.ForeignKey(ClientUser,on_delete=models.CASCADE)
    previous_job  = models.CharField(max_length=30, null=True)
    previous_compny  = models.CharField(max_length=30,null=True)
    experience_year  = models.PositiveIntegerField()
    about  = models.CharField(max_length=200)





