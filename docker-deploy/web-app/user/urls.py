from django.urls import path
from django.contrib.auth import views as login
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/',views.login,name='login'),
    path('creataccount/',views.creataccount,name='creataccount'),
    path('main/',views.main,name='main'),
    path('logout/',views.logout,name='logout'),
    path('DriverReg/',views.DriverReg,name='DriverReg'),
    path('DriverEdit/',views.DriverEdit,name='DriverEdit'),
    path('ViewInfo/',views.ViewInfo,name='ViewInfo'),
    path('EditInfo/',views.EditInfo,name='EditInfo'),
    path('RideReq/',views.RideReq,name='RideReq'),
    path('<int:nid>/EditOrder/',views.EditOrder,name='EditOrder'),
    path('FindDrive/',views.FindDrive,name='FindDrive'),
    path('<int:nid>/BeDriver/',views.BeDriver,name='BeDriver'),
    path('ViewDrive/',views.ViewDrive,name='ViewDrive'),
    path('<int:nid>/Complete/',views.Complete,name='Complete'),
    path('History/',views.History,name='History'),
    path('Join/',views.Join,name='Join'),
    path('<int:nid>/JoinIt/',views.JoinIt,name='JoinIt'),
    path('ViewOwner/',views.ViewOwner,name='ViewOwner'),
    path('ViewSharer/',views.ViewSharer,name='ViewSharer'),
]
