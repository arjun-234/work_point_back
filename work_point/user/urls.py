from django.urls import path
from .import views

urlpatterns = [

    # path('',views.list_jobs,name='job'),
    path('userqualificationview/<int:id>',views.userqualificationview.as_view()),
    path('userqual',views.userqal.as_view()),
    path('userqual/<int:pk>',views.userqualview.as_view()),
    path('user/<int:id>',views.userexpview.as_view()),
    path('userexp',views.getuserexp.as_view()),
    path('userexp/<int:pk>',views.userexperienceview.as_view()),
    path('jobview',views.jobviews.as_view()),
    path('delete_notify/<int:id>',views.Notifications.as_view(),name='delete_notify'),
    path('showstatus/<int:id>',views.Showstatus.as_view(),name='showstatus'),
    path('showstatus',views.Showstatus.as_view(),name='showstatus'),
    path('jobsearch',views.jobsearchview.as_view()),
    path('notification',views.Notifications.as_view()),

    # path('deletenotify/<int:id>',views.Notifications.as_view()),
    # path('usersearch',views.usersearchview.as_view()),
 
]










