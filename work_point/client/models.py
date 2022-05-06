from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

STATUS_TYPES = (('todo','TODO'),('inprogress','INPROGRESS'),('completed','COMPLETED'))
NOTIFICATION_TYPES = (("accept",'Accept'),('rejected','Rejected'))

class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    mobile = models.CharField(max_length=12)
    gender = models.CharField(max_length=9)
    country = models.CharField(max_length=30,blank=True)
    about = models.TextField(null=True)
    img_link = models.CharField(null=True,max_length=100)
    otp=models.IntegerField(null=True)

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    posted_date = models.CharField(max_length=20)
    is_completed = models.BooleanField(null=True)
    price = models.FloatField()
    client = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='blog_likes',blank=True)
    unlikes = models.ManyToManyField(User,related_name='blog_unlikes',blank=True)
    user = models.ManyToManyField(User,related_name='user_working_for_job',blank=True)
    is_occupied = models.BooleanField(default=False)
    
    def __str__(self):
    	return self.title
    
    def total_likes(self):
    	return self.likes.count()
    
    def total_unlikes(self):
    	return self.unlikes.count()




class Skill(models.Model):
	name = models.CharField(max_length=30)
	job = models.ManyToManyField(Job,related_name='job_skills',blank=True)
	user = models.ManyToManyField(User,related_name='user_skills',blank=True)

	def __str__(self):
		return self.name

class Proposal(models.Model):
    discription = models.TextField(blank=True)
    price = models.FloatField()
    client = models.ForeignKey(User,on_delete=models.CASCADE,related_name='proposal_client')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='proposal_user')
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=STATUS_TYPES,null=True)
    is_accepted = models.BooleanField(null=True)
    
    # def __str__(self):
    #     return self.job.title 

	# def __str__(self):
	# 	return self.job.title


class Notification(models.Model):
    proposal = models.ForeignKey(Proposal,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    client = models.ForeignKey(User,on_delete=models.CASCADE)
  


class Message(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_sender')
    reciever=models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_reciever')
    msg=models.TextField(blank=True)
    
    def __str__(self):
        return self.msg
    
class MessageCounter(models.Model):
    count=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_counter_user')
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_counter_sender')
