from email import message
from pyexpat.errors import messages
from traceback import print_tb
from django.http import HttpResponse
from django.shortcuts import render
from django.test import client
from django.db.models import Q
from client.serializers import NotificationUserSerializer
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from client.models import  Proposal, User as ClientUser
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated


class userqualificationview(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,id):
        userview = UserQualification.objects.get(id=id)
        serializer = userqualserializer(userview)
        return Response(serializer.data)


class userqal(APIView):
    permission_classes = (IsAuthenticated,)
    def  get(self,request):
        id_ = ClientUser.objects.get(username=request.data['username']).id
        userqal = UserQualification.objects.filter(user_id=id_)  
        serializer = userqualserializer(userqal,many=True)
        return Response(serializer.data)

    def post(self,request):
        request.data['user'] = ClientUser.objects.get(username=request.data['username']).id
        serializer =  userqualserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Qualification data created')
        return Response(serializer.errors) 
   

       
class userqualview(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request,pk):
        usrqual = UserQualification.objects.get(id=pk)
        serializer = userqualserializer(usrqual, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Qualification has been Updated'},status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Qualification data not update'},status=status.HTTP_406_NOT_ACCEPTABLE)
            
           
            
               
class userexpview(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,id):
        userview = UserExperience.objects.get(id=id)
        serializer = userexpserializer(userview)
        return Response(serializer.data)


class getuserexp(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        id_ = ClientUser.objects.get(username=request.data['username']).id
        usrexp = UserExperience.objects.filter(user_id=id_)  
        serializer = userexpserializer(usrexp,many=True)
        return Response(serializer.data) 
        
    def post(self,request):
        request.data['user'] = ClientUser.objects.get(username=request.data['username']).id
        serializer =  userexpserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Experience has been created",status=status.HTTP_200_OK)
        return Response({"msg":"Experience Not created"},status=status.HTTP_406_NOT_ACCEPTABLE) 
            
      
class userexperienceview(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request,pk):
        usrqual = UserExperience.objects.get(id=pk)
        serializer = userexpserializer(usrqual, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Experience data update'},status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Experience data not update'},status=status.HTTP_406_NOT_ACCEPTABLE)
      
       
class jobviews(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        jobviews = Job.objects.all().filter(is_occupied=False)
        serializer = jobviewserializer(jobviews,many=True)
        return Response(serializer.data)

class jobsearchview(generics.ListCreateAPIView):
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)
    queryset = Job.objects.all().filter(is_occupied=False)
    serializer_class = jobviewserializer


class Notifications(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        uid_ = ClientUser.objects.get(username=request.data['username']).id
        # userview = Proposal.objects.filter(user_id=uid_)
        userview = Proposal.objects.filter(Q(user_id=uid_)& Q(is_accepted = True)| Q(is_accepted = False))
        serializer = NotificationUserSerializer(userview,many=True)
        return Response(serializer.data)
       

    def delete(self,request,id):
        if id:
            delete_notify =Proposal.objects.get(id=id)
            delete_notify.delete()
            return Response({'msg':'Notifications has been Deleted'},status=200)
        else:
            return Response({'msg':'Notifications id not get'},status=200)
        

class Showstatus(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request,id):
        # uid_ = ClientUser.objects.get(username=request.data['username']).id
        proposal = Proposal.objects.get(id=id)
        serializer = Statususer(proposal, data=request.data,partial=True,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Status has been updated'},status=200)
        else:
            print(serializer.errors)
            return Response({'msg':'Status has not been updated'},status=400)    

    def get(self,request):
        uid_ = ClientUser.objects.get(username=request.data['username']).id
        proposal = Proposal.objects.filter(user_id=uid_)[::-1]
        print(proposal,"****")
        serializer = Statususer(proposal,many=True)
        return Response(serializer.data)
    
    def delete(self,request,id):
        if id:
            delete_notify = Proposal.objects.filter(id=id)
            delete_notify.delete()
            return Response({'msg':'Job has been Deleted'},status=200)
        else:
            return Response({'msg':'Status id not get'},status.HTTP_406_NOT_ACCEPTABLE)

            
      
class userqualdelete(APIView):
    def delete(self,request,pk):
        if pk:
            delete_qualification =UserQualification.objects.get(id=pk)
            delete_qualification.delete()
            return Response({'msg':'Qualification has been Deleted'},status=200)  
        else:
            return Response({'msg':'Qualification  id not get'},status.HTTP_406_NOT_ACCEPTABLE)  

class userexpdelete(APIView):
    def delete(self,request,pk):
        if pk:
            delete_exp =UserExperience.objects.get(id=pk)
            delete_exp.delete()
            return Response({'msg':'Experience has been Deleted'},status.HTTP_200_OK)  
        else:
            return Response({'msg':'Experience id not get'},status.HTTP_406_NOT_ACCEPTABLE)  


class PandingNotifications(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self,request):
        uid_ = ClientUser.objects.get(username=request.data['username']).id
        # userview = Proposal.objects.filter(user_id=uid_)
        userview = Proposal.objects.filter(Q(user_id=uid_)& Q(is_accepted = None)| Q(is_accepted = None))
        serializer = NotificationUserSerializer(userview,many=True)
        return Response(serializer.data)