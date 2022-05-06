"""work_point URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register',views.Register.as_view(),name='register'),
    path('login',views.Login.as_view(),name='login'),
    path('forgot_password',views.ForgotPassword.as_view(),name='forgot_password'),
    path('verify_otp',views.VerifyOTP.as_view(),name='verify_otp'),
    path('set_password',views.SetPassword.as_view(),name='set_password'),
    path('verify_token',views.VerifyToken.as_view(),name='verify_token'),
    path('logout',views.Logout.as_view(),name='logout'),
    path('edit_profile',views.EditProfile.as_view(),name='edit_profile'),
    path('user_details',views.UserDetails.as_view(),name='user_details'),
    path('job_post',views.JobPost.as_view(),name='job_post'),
    path('edit_job/<int:id>',views.EditJob.as_view(),name='edit_job'),
    path('get_job_detail/<int:id>',views.GetJobDetail.as_view(),name='get_job_detail'),
    path('delete_job/<int:id>',views.DeleteJob.as_view(),name='delete_job'),
    path('like_job/<int:id>',views.LikeJob.as_view(),name='like_job'),
    path('dislike_job/<int:id>',views.DislikeJob.as_view(),name='dislike_job'),
    path('asign_job/<int:id>',views.AsignJobToUser.as_view(),name='asign_job'),
    path('update_job_status/<int:id>',views.UpdateStatus.as_view(),name='update_job_status'),
    path('client_job_list',views.ClientJobList.as_view(),name='client_job_list'),
    path('make_proposal',views.MakeProposal.as_view(),name='make_proposal'),
    path('proposal_action/<int:id>',views.ProposalAction.as_view(),name='proposal_action'),
    path('skill_list',views.SkillList.as_view(),name='skill_list'),
    path('add_user_skill',views.AddUserSKill.as_view(),name='add_user_skill'),
    path('add_job_skill',views.AddJobSKill.as_view(),name='add_job_skill'),
    path('user_job_list',views.UserJobList.as_view(),name='user_job_list'),
    path('proposal_detail/<int:id>',views.ProposalDetail.as_view(),name='proposal_detail'),
    path('message_post',views.MessagePost.as_view(),name='message_post'),
    path('user_profile_search',views.UserProfileSearch.as_view(),name='user_profile_search'),
    path('user_profile_details/<int:id>',views.UserProfileDetails.as_view(),name='user_profile_details'),
    path('message_counter',views.MessageCount.as_view(),name='message_counter'),
    path('clear_message_count',views.ClearMessageCount.as_view(),name='clear_message_count'),
    path('user_details_id/<int:id>',views.UserDetailsId.as_view(),name='user_details_id'),
    path('chat_list',views.ChatList.as_view(),name='chat_list'),
    path('ChatDetails',views.ChatDetails.as_view(),name='ChatDetails'),
    path('chat_history',views.ChatHistory.as_view(),name='chat_history'),
    path('client_n',views.Clientnotfcation.as_view(),name='client_n'),   
    path('proposal_history',views.ProposalHistory.as_view(),name='proposal_history'),   
    path('client_status',views.ClientStatus.as_view(),name='client_status'),   
]
