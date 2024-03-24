"""
URL configuration for SmartInvest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ComptesSmart.views import *
from SmartInvest import settings
from django.urls import path
from django.conf.urls.static import static
from SmartInvestApp.views import *

urlpatterns = [
    path('',index,name='index'),
    path('politique/',politique,name='politique'),
    path('logout/',deconnexion,name='logout'),
    path('intro/',intro,name='intro'),
    path('inscription/',inscription,name='inscription'),
    path('connexion/',connexion,name='connexion'),
    path('profile/<str:nom>',profile,name='profile'),
    path('notifications/',notifications,name='notifications'),
    path('messages/',messages,name='messages'),
    path('parrainage/<str:nom>',parrainage,name='parrainage'),
    path('help/',help,name='help'),
    path('transactions/',transactions,name='transactions'),
    path('Annoncer/',messages,name='annoncer'),
    path('PasserAnnonce/',PasserAnnonce,name='PasserAnnonce'),
    path('utilisateurs/',utilisateurs,name='utilisateurs'),
    path('acheter/',acheter,name='acheter'),
    path('distribuer/',distribuer,name='distribuer'),
    path('retrait/',retrait,name='retrait'),
    path('valider_transaction/<str:id>',validerTransaction,name='valider_transaction'),
    path('inscriptionParrainee/<str:code>',inscriptionParrainee,name='inscriptionParrainee'),
    path('refuser_transaction/<str:id>',refuserTransaction,name='refuser_transaction'),
    path('profile/<str:nom>',profile,name='profile'),
    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"),


    path('admin/', admin.site.urls),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
