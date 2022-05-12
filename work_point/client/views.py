from django.core.mail import send_mail
from numpy import True_
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
import random
from django.conf import settings
from .serializers import *
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .JobRecommander import JobRecommander as JR 
from django.db.models import Q
from django.db.models import Count
import re
# Create your views here.




def invalid_username(username):
	if re.match(r'^(?![._])[a-zA-Z0-9_.]{5,20}$',username):
		return False
	else:
		return {"msg":{'username':["1)Username must be 5-20 characters long",\
				"2) Username may only contain:","- Uppercase and lowercase letters","- Numbers from 0-9 and",\
				"- Special characters _.","3) Username may not:Begin or finish with _ ,."]}}

class Register(APIView):
	def post(self,request):

		if User.objects.filter(email=request.data['email']).exists():
			return Response({'msg':'User with same email exists'},status=404)
		if User.objects.filter(mobile=request.data['mobile']).exists():
			return Response({'msg':'User with same mobile no. exists'},status=404)
		if User.objects.filter(username=request.data['username']).exists():
			return Response({'msg':'User with same username exists'},status=404)
		else:
			reg_error=[]
			if re.match(r'^(?![._])[a-zA-Z0-9_.]{5,20}$',request.data['username']):
				pass
			else:
				reg_error.append({'username':["1)Username must be 5-20 characters long",\
				"2) Username may only contain:","- Uppercase and lowercase letters","- Numbers from 0-9 and",\
				"- Special characters _.","3) Username may not:Begin or finish with _ ,."]})

			if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',request.data['email']):
				pass
			else:
				reg_error.append({'email':'Invalid Email'})
			if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$",request.data['password']):
				pass
			else:
				reg_error.append({'password':["at least one digit","at least one uppercase letter","at least one lowercase letter","at least one special character[$@#]"]})
			if re.match(r"(0|91)?[7-9][0-9]{9}",request.data['mobile']):
				pass
			else:
				reg_error.append({'Mobile':"Invalid Mobile Number"})
			if len(reg_error)==0:

				serializer = RegisterSerializer(data=request.data,many=False)
				if serializer.is_valid():
					serializer.save()
					return Response({'msg':'User has been registered'},status=200)
				else:
					return Response(serializer.errors)
			else:
				return Response({'msg':reg_error},status=406)

class Login(APIView):
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				obj = authenticate(username=request.data['username'],password=request.data['password'])
				if obj is not None:
					user = User.objects.get(username=request.data['username'])
					serializer = LoginSerializer(user,many=False)
					return Response(serializer.data,status=200)
				else:
					return Response({'msg':'Invalid credentials'},status=404)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class Logout(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				obj = Token.objects.get(user=user)
				obj.delete()
				return Response({'msg':'Successfully Logout'},status=200)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class VerifyToken(APIView):
	
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				token = Token.objects.get(user=user)
				if token.key == request.data['token']:
					return Response({'matched':True,'msg':'Valid Token'})
				else:
					return Response({'matched':False,'msg':'Invalid Token'})
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class ForgotPassword(APIView):
	
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user =  User.objects.get(username=request.data['username'])
				otp = random.randint(111111,999999)
				user.otp=otp
				user.save()
				subject = 'Reset password'
				message = f'Hi {user.first_name}, Your OTP for resetting your password is {otp}.'
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [user.email]
				send_mail( subject, message, email_from, recipient_list )
				return Response({'msg':'OTP has been sent.','email':user.email})
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class VerifyOTP(APIView):

	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user =  User.objects.get(username=request.data['username'])
				if request.data['user_otp'] == user.otp:
					user.otp=None
					user.save()
					return Response({"matched":True,"msg":"OTP matched"},status=200)
				else:
					user.otp=None
					user.save()
					return Response({"matched":False,"msg":"OTP doesn't match"},status=200) 
				
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class SetPassword(APIView):
	
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				reg_error=[]
				if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$",request.data['password']):
					pass
				else:
					reg_error.append({'password':["at least one digit","at least one uppercase letter","at least one lowercase letter","at least one special character[$@#]"]})
				if len(reg_error)==0:	
					user = User.objects.get(username__exact=request.data['username'])
					print(request.data['password'],"@@@@@@@@@@@@@@@@@@")
					user.set_password(request.data['password'])
					user.save()
					return Response({'msg':"Password has changed"})
				else:
					return Response({'msg':reg_error})
			else:
				return Response({'msg':"username doesn't exist"},status=404)

class EditProfile(APIView):
	permission_classes = (IsAuthenticated,)
	def put(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				reg_error=[]
				try:

					if re.match(r"(0|91)?[7-9][0-9]{9}",request.data['mobile']):
						pass
					else:
						reg_error.append({'Mobile':"Invalid Mobile Number"})
				except:
					pass
				if len(reg_error)==0:
					serializer = RegisterSerializer(data=request.data,many=False,instance=user,partial=True)
					if serializer.is_valid():
						serializer.save()
						return Response({'msg':'User has been updated'},status=200)
					else:
						return Response(serializer.errors)
				else:
					return Response({'msg':reg_error})
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class UserDetails(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				serializer = UserSerializer(user)
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class JobPost(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				request.data['client'] = User.objects.get(username=request.data['username']).id
				serializer = JobSerializer(data=request.data,many=False)
				if serializer.is_valid():
					serializer.save()
					return Response({'msg':'Job has been Posted','job_id':serializer.data['id']},status=200)
				else:
					return Response(serializer.errors)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class EditJob(APIView):
	permission_classes = (IsAuthenticated,)
	def put(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				job = Job.objects.get(id=id) 
				serializer = JobSerializer(data=request.data,many=False,instance=job,partial=True)
				if serializer.is_valid():
					serializer.save()
					return Response({'msg':'Job has been Updated'},status=200)
				else:
					return Response(serializer.errors)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class GetJobDetail(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				job = Job.objects.get(id=id) 
				serializer = GetJobClientSideSerializer(job)
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class DeleteJob(APIView):
	permission_classes = (IsAuthenticated,)
	def delete(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				job = Job.objects.get(id=id) 
				job.delete()
				return Response({'msg':'Job has been Deleted'},status=200)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class LikeJob(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				if Job.objects.filter(id=id).exists():
					job = Job.objects.get(id=id)
					if job.likes.filter(id=user.id).exists():
						job.likes.remove(user)
						return Response({'msg':'Remove Like Successfully'})
					else:
						job.likes.add(user)
						if job.unlikes.filter(id=user.id).exists():
							job.unlikes.remove(user)
						return Response({'msg':'Job has been liked Successfully'})
				else:
					return Response({"msg":"Invalid Job Id"},status=404)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class DislikeJob(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				if Job.objects.filter(id=id).exists():
					job = Job.objects.get(id=id)
					if job.unlikes.filter(id=user.id).exists():
						job.unlikes.remove(user)
						return Response({'msg':'Remove Unlike Successfully'})
					else:
						job.unlikes.add(user)
						if job.likes.filter(id=user.id).exists():
							job.likes.remove(user)
						return Response({'msg':'Job has been Unliked Successfully'})
				else:
					return Response({"msg":"Invalid Job Id"},status=404)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class AsignJobToUser(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				if Job.objects.filter(id=id).exists():
					job = Job.objects.get(id=id)
					Job.objects.filter(id=id).update(is_occupied=True)
					if not job.user.filter(id=user.id).exists():
						job.user.add(user)
						return Response({"msg":"Work Has been asigned to particular user"})
					else:
						return Response({"msg":"Work Has been asigned to particular user"})
				else:
					return Response({"msg":"Invalid Job Id"},status=404)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class UpdateStatus(APIView):
	permission_classes = (IsAuthenticated,)
	def put(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if Job.objects.filter(id=id).exists():
				job = Job.objects.get(id=id)
				serializer = JobSerializer(data=request.data,many=False,instance=job,partial=True)
				if serializer.is_valid():
					serializer.save()
					return Response({"msg":"Status has been updated"})
				else:
					return Response(serializer.errors)
			else:
				return Response({"msg":"Invalid Job Id"},status=404)

class ClientJobList(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				job_list = Job.objects.filter(client_id=user.id)
				serializer = GetJobClientSideSerializer(job_list,many=True)
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class MakeProposal(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				request.data['client'] = Job.objects.get(id=request.data['job']).client.id
				request.data['user'] = User.objects.get(username=request.data['username']).id
				if Proposal.objects.filter(Q(job_id=request.data['job']) & Q(user_id = request.data['user'])).exists():
					prop_obj = Proposal.objects.filter(Q(job_id=request.data['job']) & Q(user_id = request.data['user']))[0]
					prop_obj.is_accepted = None
					prop_obj.save()
					serializer = MakeProposalSerializer(data = request.data,many=False,instance=prop_obj)
					jobobj=Job.objects.get(id=request.data['job'])
					if int(jobobj.price) >= int(request.data['price']) and int(request.data['price']) != 0:
						if serializer.is_valid():
							serializer.save()
							return Response({'msg':'Proposal has been made'})
						else:
							return Response(serializer.errors)
					else:
						return Response({'msg':f'Price must be in range of 1 to {int(jobobj.price)}'})
				else:

					serializer = MakeProposalSerializer(data = request.data,many=False)
					jobobj=Job.objects.get(id=request.data['job'])
					if int(jobobj.price) >= int(request.data['price']) and int(request.data['price']) != 0:
						if serializer.is_valid():
							serializer.save()
							return Response({'msg':'Proposal has been made'})
						else:
							return Response(serializer.errors)
					else:
						return Response({'msg':f'Price must be in range of 1 to {int(jobobj.price)}'})
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class ProposalAction(APIView):
	permission_classes = (IsAuthenticated,)
	def put(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				obj = Proposal.objects.get(id=id)
				job = Job.objects.get(id=obj.job.id)
				proposarobj=User.objects.get(id=obj.user.id)
				print(user,'user')
				if Job.objects.filter(id=obj.job.id).exists():
					print(obj)
					serializer = MakeProposalSerializer(data=request.data,instance=obj,partial=True)
					if serializer.is_valid():
						serializer.save()
						print(request.data['is_accepted'])
						if request.data['is_accepted'] == "True":
							job.is_occupied=True
							job.save()
							if not job.user.filter(id=proposarobj.id).exists():
								job.user.add(proposarobj)
						return Response({'msg':'Proposal has been accepted/rejected'})
					else:
						return Response(serializer.errors)
				else:
					return Response({'msg':'Invalid ID'},status=404)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class SkillList(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request):
		obj = Skill.objects.all()
		serializer = SkillSerializer(obj,many=True)
		return Response(serializer.data)

class AddUserSKill(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				for i in Skill.objects.all():
					if Skill.objects.get(name=i.name).user.filter(id=user.id).exists():
						Skill.objects.get(name=i.name).user.remove(user)
				for i in request.data['skill_list']:
					if Skill.objects.filter(name=i).exists():
						if Skill.objects.get(name=i).user.filter(id=user.id).exists():
							pass
						else:
							Skill.objects.get(name=i).user.add(user)
				return Response({'msg':'skill has been set for user'})
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class AddJobSKill(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		if Job.objects.filter(id=request.data['job']).exists():
			job = Job.objects.get(id=request.data['job'])
			for i in Skill.objects.all():
				if Skill.objects.get(name=i.name).job.filter(id=job.id).exists():
					Skill.objects.get(name=i.name).job.remove(job)
			for i in request.data['skill_list']:
				if Skill.objects.filter(name=i).exists():
					if Skill.objects.get(name=i).job.filter(id=job.id).exists():
						pass
					else:
						Skill.objects.get(name=i).job.add(job)
			return Response({'msg':'skill has been set for Job'})
		else:
			return Response({'msg':'Invalid Job ID'},status=404)

class UserJobList(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				user = User.objects.get(username=request.data['username'])
				skill_obj = Skill.objects.filter(user=user)
				skill_list=[i.name for i in skill_obj]
				if len(skill_list)<1:
					job_list = Job.objects.filter(is_occupied=False)
					serializer = JobSerializer(job_list,many=True)
					return Response(serializer.data[::-1])
				else:
					try:
						recommander = JR()
						recommanded_jobs = recommander.give_job_recommandation(username=user.username,skill_list=skill_list)
						job_list = Job.objects.filter(id__in=tuple(recommanded_jobs)).filter(is_occupied=False)
						qs_sorted = list()
						for i in recommanded_jobs:
							try:
								qs_sorted.append(job_list.get(id=i))
							except:
								pass
						serializer = JobSerializer(qs_sorted,many=True)
						return Response(serializer.data)
					except:
						print("***** NO records in db. first, insert record to run JobRecommander system *****")
						job_list = Job.objects.filter(is_occupied=False)
						serializer = JobSerializer(job_list,many=True)
						return Response(serializer.data[::-1])
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class ProposalDetail(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				obj = Proposal.objects.filter(job_id=id).get(user_id=request.data['proposer_id'])
				serializer = ProposalDetailSerializer(obj)
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)



class MessagePost(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				request.data['sender']=User.objects.get(username=request.data['username']).id
				serializer=MessageSerializer(data=request.data)
				if len(request.data['msg'].strip())!=0:
					if serializer.is_valid():
						serializer.save()
						request.data['user']=request.data['reciever']
						request.data['count']=1
						if MessageCounter.objects.filter(sender=request.data['sender']).filter(user=request.data['user']).exists():
							obj=MessageCounter.objects.filter(sender=request.data['sender']).filter(user=request.data['user'])[0]
							# return Response({"id":obj.count})
							request.data['count']=obj.count+1
							print(request.data['count'],"@@@@")
							serializer=MessageCounterSerializer(data=request.data,instance=obj)
							if serializer.is_valid():

								serializer.save()
							else:
								return Response(serializer.errors)
						else:
							serializer=MessageCounterSerializer(data=request.data)
							if serializer.is_valid():

								serializer.save()
							else:
								return Response(serializer.errors)

						return Response({'msg':'Message Has been sent!'})
					else:
						return Response(serializer.errors) 
				else:
					return Response({'msg':'blank Message Has been sent!'})
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class ChatList(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				smobj=User.objects.get(username=request.data['username'])
				obj=Message.objects.filter(Q(sender_id=smobj.id)|Q(reciever_id=smobj.id))
				serializer=ChatListSerializer(obj,many=True)
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)



class UserDetailsId(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				obj=User.objects.get(id=id)
				serializer=UserDetailsIdSerializer(obj,many=False)
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

#message Counter
class MessageCount(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				userobj=User.objects.get(username=request.data['username'])
				msgobj=MessageCounter.objects.filter(user_id=userobj.id)
				serializer=MessageCounterSerializer(msgobj,many=True)
				return Response(serializer.data)	
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class ClearMessageCount(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				userobj=User.objects.get(username=request.data['username'])
				obj=MessageCounter.objects.filter(sender_id=request.data['sender']).filter(user_id=userobj.id)[0]
				obj.count = 0
				obj.save()
				# serializer.data['count']=0
				return Response({"msg":" has been reset"})
				
			else:
				return Response({'msg':'No account associated with given username'},status=404)



class ChatDetails(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				return Response({""})
			else:
				return Response({'msg':'No account associated with given username'},status=404)




class UserProfileSearch(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				qry=User.objects.filter(Q(username__icontains = request.data['input'])|Q(first_name__icontains = request.data['input'])|Q(last_name__icontains = request.data['input']))
				serializer=UserSearchResultSerializer(qry,many=True)
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)
				
	

class ChatHistory(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				qry=User.objects.filter(Q(username=request.data['username'])|Q(id=request.data['id'])|Q()|Q())
				print()
			else:
				return Response({'msg':'No account associated with given username'},status=404)


		
class Clientnotfcation(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				cid_ = User.objects.get(username=request.data['username']).id
				clientview = Proposal.objects.filter(Q(client_id=cid_)&Q(is_accepted = None))
				print(clientview,"((()))")
				# print(c.is_accepted,"uuuuuhhh")
			
				serializer = ClientnotificationSerializer(clientview,many=True)
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class UserProfileDetails(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request,id):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				qry=User.objects.filter(id=id)
				serializer=UserProfileDetailsSerializer(qry,many=True)
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)



class ProposalHistory(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				userobj=User.objects.get(username=request.data['username'])
				obj=Proposal.objects.filter(client_id=userobj.id).filter(Q(is_accepted=True)|Q(is_accepted=False))
				serializer=PropesalHistorySerializer(obj,many=True)	
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class ClientStatus(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				userobj=User.objects.get(username=request.data['username'])
				proposalobj=Proposal.objects.filter(client_id=userobj.id).filter(is_accepted=True)

				serializer=PropesalHistorySerializer(proposalobj,many=True)	
				return Response(serializer.data)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class JobDetails(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				if Job.objects.filter(id=request.data['job']).exists():
					jobobj=Job.objects.get(id=request.data['job'])
					serializer=JobSerializer(jobobj)
					return Response(serializer.data)
				else:
					return Response({'msg':'Invalid Job ID'},status=404)
			else:
				return Response({'msg':'No account associated with given username'},status=404)

class GiveRating(APIView):
	def post(self,request):
		try:
			usernameobj=request.data['username']
		except:
			return Response({'msg':'Username Required'})
		if invalid_username(request.data['username']):
			return Response(invalid_username(request.data['username']),status=406)
		else:
			if User.objects.filter(username=request.data['username']).exists():
				if Job.objects.filter(id=int(request.data['job'])).exists():
					if User.objects.filter(id=int(request.data['user'])).exists():
						if int(request.data['number']) in range(6):
							if Rating.objects.filter(job_id=int(request.data['job'])).filter(user_id=int(request.data['user'])).exists():
								raitng_obj = Rating.objects.filter(job_id=int(request.data['job'])).filter(user_id=int(request.data['user']))[0]
								serializer = GiveRatingSerializer(data=request.data,instance=raitng_obj)
								if serializer.is_valid():
									serializer.save()
									return Response({'msg':f"You have Successfully given {request.data['number']} star"})
								else:
									return Response(serializer.errors)
							else:
								serializer = GiveRatingSerializer(data=request.data)
								if serializer.is_valid():
									serializer.save()
									return Response({'msg':f"You have Successfully given {request.data['number']} star"})
								else:
									return Response(serializer.errors)
						else:
							return Response({'msg':'Invalid Rating Number(1-5)'},status=404)
					else:
						return Response({'msg':'Invalid user ID'},status=404)
				else:
					return Response({'msg':'Invalid Job ID'},status=404)
			else:
				return Response({'msg':'No account associated with given username'},status=404)
