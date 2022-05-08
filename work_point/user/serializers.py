
from client.models import Job, Proposal, User
from .models import *
from rest_framework import serializers




class  userqualserializer(serializers.ModelSerializer):
    class Meta:
        model = UserQualification
        fields = ['id','user','recent_degree','cpi','passing_year','university','about']


class  userexpserializer(serializers.ModelSerializer):
    class Meta:
        model = UserExperience
        fields = ['id','user','previous_job','previous_compny','experience_year','about']

class jobviewserializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    class Meta:
        model =  Job
        fields = ['id','title','description','posted_date','price','client','likes','unlikes','is_occupied','user','is_completed','client_name']

    def get_client_name(self,obj):
        user = User.objects.get(id=obj.client.id)
        return user.first_name+' '+user.last_name


class jobserializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class Statususer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()

    class Meta:
        model = Proposal
        fields = fields = ['id','job','is_accepted','client','status']
    def get_client(self,instance):
        return instance.client.username
    def get_job(self,instance):
        return instance.job.title

