from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.indexview, name="indexview"),
    path('registration/', views.registration, name="registration"),
    path('signin/', views.signin, name="signin"),
    
    path('userdashboard/', views.userdashboard, name="userdashboard"),
    path('userprogramview/', views.userprogramview, name="userprogramview"),
    path('usersearchview/', views.usersearchview, name="usersearchview"),
    path('userorganisationview/', views.userorganisationview, name="userorganisationview"),
    path('userfeedbackview/', views.userfeedbackview, name="userfeedbackview"),
    path('userdonationview/', views.userdonationview, name="userdonationview"),
    
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('admindashboard/', views.admindashboard, name="admindashboard"),

    
    path('searchresult_petshop2/', TemplateView.as_view(template_name="searchresult_petshop2.html"), name='searchresult_petshop2'),

    path(r'^export/csv/$', views.export_users_csv, name='export_users_csv'),
    path(r'^export/csv/$', views.export_users_csv_feed, name='export_users_csv_feed'),
    path(r'^export/csv/$', views.export_users_csv_donate, name='export_users_csv_donate')
]
#path('usersearchdataview/', views.usersearchdataview, name='usersearchdataview'),
