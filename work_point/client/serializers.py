# from attr import fields
from django.dispatch import receiver
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from .models import *
from user.models import *
from user.serializers import *


class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

	def validate_password(self,password):
		return make_password(password)


class LoginSerializer(serializers.ModelSerializer):
	token = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ['username','img_link','first_name','is_client','token']
	
	def get_token(self,obj):
		token,_ = Token.objects.get_or_create(user=obj)
		return token.key

class SkillSerializer(serializers.ModelSerializer):
	class Meta:
		model = Skill
		fields = ['id','name']
		
class UserSerializer(serializers.ModelSerializer):
	token = serializers.SerializerMethodField()
	skill=serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ['username','first_name','last_name','gender','country','email','mobile','is_client','about','img_link','token','skill']
	

	
	def get_token(self,obj):
		token,_ = Token.objects.get_or_create(user=obj)
		return token.key

	def get_skill(self,obj):
		data = Skill.objects.filter(user=obj.id)
		serializer = SkillSerializer(data,many=True)
		return serializer.data

class JobSerializer(serializers.ModelSerializer):
	skill=serializers.SerializerMethodField()
	client_name=serializers.SerializerMethodField()
	class Meta:
		model = Job
		fields = ['id','title','description','posted_date','is_completed','price','is_occupied','client','likes','unlikes','user','skill','client_name']

	def get_skill(self,obj):
		data = Skill.objects.filter(job=obj.id)
		serializer = SkillSerializer(data,many=True)
		return serializer.data

	def get_client_name(self,obj):
		data=User.objects.get(id=obj.client.id)
		return data.first_name+' '+data.last_name



class UserOnClientSidePostSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','username','first_name','last_name']
		
class GetJobClientSideSerializer(serializers.ModelSerializer):
	user = UserOnClientSidePostSerializer(many=True)
	skill = serializers.SerializerMethodField()
	class Meta:
		model = Job
		fields = ['id','title','description','posted_date','is_completed','price','likes','unlikes','user','skill']
	
	def get_skill(self,obj):
		data = Skill.objects.filter(job=obj.id)
		serializer = SkillSerializer(data,many=True)
		return serializer.data

class MakeProposalSerializer(serializers.ModelSerializer):
	class Meta:
		model=Proposal
		fields='__all__'
	
class NotificationUserSerializer(serializers.ModelSerializer):
	job = serializers.SerializerMethodField()
	client = serializers.SerializerMethodField()
	class Meta:
		model = Proposal
		fields = ['id','discription', 'price', 'client', 'user', 'job', 'is_accepted']

	def get_job(self, instance):
		#print(instance, "????")
		return instance.job.title

	def get_client(self, instance):
		#print(instance, "????")
		return instance.client.username		

class ProposalDetailSerializer(serializers.ModelSerializer):
	job = JobSerializer()
	skill = serializers.SerializerMethodField()
	user_skill=serializers.SerializerMethodField()
	user_name=serializers.SerializerMethodField()
	class Meta:
		model = Proposal
		fields = ['id','user','discription','price','skill','job','user_name','user_skill']
	def get_skill(self,obj):
		data = Skill.objects.filter(job=obj.job.id)
		serializer = SkillSerializer(data,many=True)
		return serializer.data
	def get_user_skill(self,obj):
		data=Skill.objects.filter(user=obj.user.id)
		serializer=SkillSerializer(data,many=True)
		return serializer.data
	def get_user_name(self,obj):
		data=User.objects.get(id=obj.user.id)
		return data.username

class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model=Message
		fields='__all__'

class MessageCounterSerializer(serializers.ModelSerializer):
	class Meta:
		model=MessageCounter
		fields='__all__'

class UserSearchResultSerializer(serializers.ModelSerializer):
	skill = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ['id','username','first_name','last_name','gender','country','email','mobile','is_client','about','img_link','skill']

	def get_skill(self,obj):
		data = Skill.objects.filter(user=obj.id)
		serializer = SkillSerializer(data,many=True)
		return serializer.data

class UserChatListSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','username','first_name','last_name','img_link']

class ChatListSerializer(serializers.ModelSerializer):
	sender=UserChatListSerializer()
	reciever=UserChatListSerializer()
	class Meta:
		model=Message
		fields=['msg','sender','reciever']

	# def get_sender(self,obj):
	# 	data=User.objects.filter(id=obj.sender.id)
	# 	serializer=UserSerializer(data)
	# 	return serializer.data
	# def get_receiver(self,obj):
	# 	data=User.objects.filter(id=obj.receiver.id)
	# 	serializer=UserSerializer(data)
	# 	return serializer.data


# class ClientnotificationSerializer(serializers.ModelSerializer):
# 	user = serializers.SerializerMethodField()
# 	job = serializers.SerializerMethodField()
# 	class Meta:
# 		model = Proposal
# 		fields = ['id','discription','price','job','is_accepted',"user"]
# 	def get_user(self,instance):
# 		return instance.user.username
# 	def get_job(self,instance):
# 		return instance.job.title
class UserSerializerwithid(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id']
class JobSerializerwithid(serializers.ModelSerializer):
	class Meta:
		model = Job
		fields = ['id']
		
class ClientnotificationSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	job = serializers.SerializerMethodField()
	user_id = serializers.SerializerMethodField()
	job_id = serializers.SerializerMethodField()
	class Meta:
		model = Proposal
		
		fields = ['id','discription','price','job','is_accepted',"user","user_id","job_id"]
	def get_user(self,instance):
		return instance.user.username
	def get_job(self,instance):
		return instance.job.title
	def get_user_id(self,instance):
		obj=User.objects.get(id=instance.user.id)
		user_id = UserSerializerwithid(obj,many=False)
		return user_id.data
	def get_job_id(self,instance):
		obj=Job.objects.get(id=instance.job.id)
		job_id = JobSerializerwithid(obj,many=False)
		return job_id.data

class UserProfileDetailsSerializer(serializers.ModelSerializer):
	skill = serializers.SerializerMethodField()
	userqual=serializers.SerializerMethodField()
	userexp=serializers.SerializerMethodField()


	class Meta:
		model=User
		fields=['id','username','first_name','last_name','country','email','mobile','skill','userqual','userexp','img_link','about']

	def get_skill(self,obj):
		data = Skill.objects.filter(user=obj.id)
		serializer = SkillSerializer(data,many=True)
		return serializer.data
	def get_userqual(self,obj):
		data=UserQualification.objects.filter(user=obj.id)
		serializer =userqualserializer(data,many=True)
		return serializer.data
	def get_userexp(self,obj):
		data=UserExperience.objects.filter(user=obj.id)
		serializer =userexpserializer(data,many=True)
		return serializer.data

class UserDetailsIdSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username','first_name','last_name','img_link']
	
class PropesalHistorySerializer(serializers.ModelSerializer):
	job=JobSerializer()
	user=UserSerializer()
	class Meta:
		model=Proposal
		fields=['user','job','status','is_accepted','discription','price','feedback']