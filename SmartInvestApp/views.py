import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from ComptesSmart.models import Utilisateur
from SmartInvestApp.models import *
import json
from SmartInvestApp.forms import *
from SmartInvestApp.utiles import Verifier, distribuerGains, extraire_informations_historique, recuperer_transactions_utilisateur, trouver_contrat_suivant
# Create your views here.


def intro(request):

    return render(request,'SmartInvestApp/intro.html')


def index(request):
    if not request.user.is_authenticated:
        return redirect('intro')
    print(request.user.historique_solde.split("#"))
    montants, dates = extraire_informations_historique(request.user.historique_solde)
    montantTransacts, dateTransacts, typeTransacts = recuperer_transactions_utilisateur(request.user.username)
    transactions=Transaction.objects.filter(Auteur=request.user).order_by('date')
    contrat_suivant=trouver_contrat_suivant(Contrat.objects.all(),request.user.contrat_courant)
    infos=get_object_or_404(Information,id=1)
    totalContrats=0
    totalSoldes=0
    totalUsers=0
    totalContractaires=0
    notificationss=Notification.objects.all().order_by('-date')[:4]
    Messagess=Message.objects.all().order_by('-date') [:5]
    if request.user.is_superuser :
        allUtilisateurs=Utilisateur.objects.filter(contrat_expire=False,contrat_courant__Montant__gte=0)
        allUtilisateurs2=Utilisateur.objects.all()
        totalUsers=len(allUtilisateurs2)
        for util in allUtilisateurs:
            
            if util.contrat_courant:
                
                totalContrats+=util.contrat_courant.Montant
            
        for util in allUtilisateurs2:
                totalSoldes+=util.solde
                if util.contrat_courant and not util.contrat_expire:
                    totalContractaires+=1
           
    # Sérialisation des données en JSON
    montantTransacts_json=json.dumps(montantTransacts)
    dateTransacts_json=json.dumps(dateTransacts)
    typeTransacts_json=json.dumps(typeTransacts)
    montants_json = json.dumps(montants)
    dates_json = json.dumps(dates)
    return render(request,'SmartInvestApp/index.html',context={'montants' : montants_json,"dates" : dates_json,"typeTransacts" : typeTransacts_json,"montantTransacts" : montantTransacts_json,"dateTransacts" : dateTransacts_json,"transactions" : transactions,"contrat_suivant":contrat_suivant,"infos":infos,"totalContrats":totalContrats,"totalSoldes":totalSoldes,"totalUsers":totalUsers,"totalContractaires":totalContractaires,'notificationss' : notificationss,'Messagess' : Messagess})

def politique(request):
    notificationss=Notification.objects.all().order_by('-date')[:4]
    Messagess=Message.objects.all().order_by('-date') [:5]
    return render(request,'SmartInvestApp/politique.html',context={'notificationss' : notificationss,"Messagess" : Messagess})


def parrainage(request,nom):
    if not request.user.is_authenticated:
        return redirect('connexion')
    fieuils=len(Utilisateur.objects.filter(parrain=request.user))
    notificationss=Notification.objects.all().order_by('-date')[:4]
    Messagess=Message.objects.all().order_by('-date') [:5]
    return render(request,'SmartInvestApp/parrainage.html',context={'fieuils':fieuils,'notificationss' : notificationss,"Messagess" : Messagess})

def notifications(request):
    if not request.user.is_authenticated:
        return redirect('connexion')
    notificationss=Notification.objects.all().order_by('-date')
    Messagess=Message.objects.all().order_by('-date') [:5]
    return render(request,'SmartInvestApp/notification.html',context={'notificationss' : notificationss,"Messagess" : Messagess})

def help(request):
    notificationss=Notification.objects.all().order_by('-date')[:4]
    Messagess=Message.objects.all().order_by('-date') [:5]
    return render(request,'SmartInvestApp/help.html',context={'notificationss' : notificationss,"Messagess" : Messagess})

def messages(request):
    if not request.user.is_authenticated:
        return redirect('connexion')
    Messagess=Message.objects.all().order_by('-date')
    notificationss=Notification.objects.all().order_by('-date')[:4]
    if request.method == 'POST' and request.user.is_superuser:
        Messagess=Messagess[:5]
        image=request.FILES.get("image")
        titre=request.POST.get("titre")
        contenu=request.POST.get("contenu")
        nomAuteur=request.POST.get("nomAuteur")
        
        Message.objects.create(image=image,title=titre,contenu=contenu,NomAuteur=nomAuteur)
        return redirect('messages')
    
    return render(request,'SmartInvestApp/messages.html',context={'Messagess' : Messagess,'notificationss' : notificationss})

def transactions(request):
    if not request.user.is_superuser:
        return redirect('connexion')
    
    transactions=Transaction.objects.all().order_by('-date')
    notificationss=Notification.objects.all().order_by('-date')[:4]
    Messagess=Message.objects.all().order_by('-date') [:5]
    return render(request,'SmartInvestApp/TRANSACTIONS.html',context={'transactions' : transactions,'notificationss' : notificationss,"Messagess" : Messagess})

def PasserAnnonce(request):
    if not request.user.is_superuser:
        return redirect('connexion')
    
    notificationss=Notification.objects.all().order_by('-date')[:4]
    Messagess=Message.objects.all().order_by('-date') [:5]
    return render(request,'SmartInvestApp/Annoncer.html',context={'notificationss' : notificationss,"Messagess" : Messagess})
def utilisateurs(request):
    if not request.user.is_superuser:
        return redirect('connexion')
    utilisateurs=Utilisateur.objects.all().order_by('-date')
    notificationss=Notification.objects.all().order_by('-date')[:4]
    Messagess=Message.objects.all().order_by('-date') [:5]
    return render(request,'SmartInvestApp/UTILISATEURS.html',context={'utilisateurs' : utilisateurs,'notificationss' : notificationss,"Messagess" : Messagess})

def acheter(request):
    if request.method=="POST":
        PorteFeuille =request.POST.get("adresseUSDT")
        
        Montant =request.POST.get("Montant").replace(',','.')
        MontantUSDT =request.POST.get("MontantUSDT").replace(',','.')
        contrat =float(request.POST.get("contrat").replace(',','.'))
        Numero=request.POST.get("Numero")
        Auteur=request.user
        Type='ACHAT'
        
        
        if PorteFeuille and PorteFeuille!="":
           transaction= Transaction.objects.create(PorteFeuille=PorteFeuille,Montant=Montant,MontantUSDT=MontantUSDT,contrat=contrat,Auteur=Auteur,Type=Type)
        else:
           transaction= Transaction.objects.create(Montant=Montant,contrat=contrat,Numero=Numero,Auteur=Auteur,Type=Type)
        
        #transaction.save()  
         
        return redirect('index')
    if not request.user.is_authenticated:
        return redirect('connexion')
    contrats=Contrat.objects.all().order_by('Montant')
    notificationss=Notification.objects.all().order_by('-date')[:4]
    Messagess=Message.objects.all().order_by('-date') [:5]
    return render(request,'SmartInvestApp/AcheterCOntrat.html',context={'contrats' : contrats,'notificationss' : notificationss,"Messagess" : Messagess})

def retrait(request):
    notificationss=Notification.objects.all().order_by('-date')[:4]
    Messagess=Message.objects.all().order_by('-date') [:5]
    solde=float(request.user.solde)
    prixUSDT=float(get_object_or_404(Information,id=1).prixUSDT)
    if request.method=="POST":
        PorteFeuille =request.POST.get("adresseUSDT")
        Montant =float(request.POST.get("Montant").replace(',','.'))
        MontantUSDT = float(request.POST.get("MontantUSDT").replace(',','.'))/prixUSDT
        Numero=request.POST.get("Numero")
        Auteur=request.user
        Type='RETRAIT'
        if PorteFeuille and PorteFeuille!="":
           transaction= Transaction.objects.create(PorteFeuille=PorteFeuille,Montant=Montant,MontantUSDT=MontantUSDT,Auteur=Auteur,Type=Type)
        else:
           transaction= Transaction.objects.create(Montant=Montant,Numero=Numero,Auteur=Auteur,Type=Type)
        
        return redirect('index')
    if not request.user.is_authenticated:
        return redirect('connexion')
    return render(request,'SmartInvestApp/retrait.html',context={'notificationss' : notificationss,"Messagess" : Messagess,"solde":solde,"prixUSDT":prixUSDT})

def distribuer(request):
    if not request.user.is_superuser:
        return redirect('connexion')
    Verifier()
    if request.method=="POST":
        contrat =request.POST.get("contrat")
        pourcentage =float(request.POST.get("pourcentage").replace(',','.'))
        jours=request.POST.get("jours")
        distribuerGains(pourcentage,jours,contrat)
        return redirect('index')
    notificationss=Notification.objects.all().order_by('-date')[:4]
    Messagess=Message.objects.all().order_by('-date') [:5]
    contrats=Contrat.objects.all().order_by('Montant')
    return render(request,'SmartInvestApp/distribuer.html',context={'notificationss' : notificationss,"Messagess" : Messagess,"contrats" : contrats})


############# fonctions CRUD ##############
############# fonctions CRUD ##############
############# fonctions CRUD ##############


def validerTransaction(request, id):
    # Pour valider une transaction
    if not request.user.is_superuser:
        return redirect('intro')
    
    transaction_a_valider = Transaction.objects.get(id=id)
    transaction_a_valider.valider_transaction()
    
    if transaction_a_valider.Type == 'ACHAT':
        # Récupérer le contrat acheté en fonction du montant de la transaction
        contrat_achete = get_object_or_404(Contrat, Montant=transaction_a_valider.Montant)
        # Mettre à jour le contrat courant de l'utilisateur avec le contrat acheté
        transaction_a_valider.Auteur.contrat_courant = contrat_achete
        transaction_a_valider.Auteur.date_contrat=datetime.date.today()
        transaction_a_valider.Auteur.save()
    
    elif transaction_a_valider.Type == 'RETRAIT':
        # Vérifier si le montant de la transaction est inférieur à 98% du solde de l'utilisateur
        if transaction_a_valider.Montant <= transaction_a_valider.Auteur.solde * 0.98:
            # Diminuer le solde de l'utilisateur du montant de la transaction
            transaction_a_valider.Auteur.solde -= transaction_a_valider.Montant
            ajout_historique=str(transaction_a_valider.Auteur.solde)+"|"+datetime.date.today().strftime("%d-%m-%Y")+"#"
            transaction_a_valider.Auteur.historique_solde+=ajout_historique
            transaction_a_valider.Auteur.save()
    
    return redirect('transactions')


def refuserTransaction(request,id):
    if not request.user.is_superuser:
        return redirect('intro')
    transaction_a_refuser = Transaction.objects.get(id=id)
    transaction_a_refuser.refuser_transaction()

    return redirect('transactions')










############# fonctions CRUD ##############
############# fonctions CRUD ##############
############# fonctions CRUD ##############

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/10.9.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyBdT5JVHUcNYRub3dsFUKRiIf8Xm8ZYU6E",' \
         '        authDomain: "smart-invest-f557b.firebaseapp.com",' \
         '        projectId: "smart-invest-f557b",' \
         '        storageBucket: "smart-invest-f557b.appspot.com",' \
         '        messagingSenderId: "166471964412",' \
         '        appId: "1:166471964412:web:046e9786fa06d85cc1a979",' \
         '        measurementId: "G-TZPJBC9EGM"' \
         ' };' \
         'app=initializeApp(firebaseConfig);' \
         'const messaging=getMessaging(app);' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")