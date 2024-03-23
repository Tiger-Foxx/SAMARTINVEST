import datetime
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model,login,logout,authenticate
import django.contrib.auth.models
from django.http import JsonResponse
import random
import string
# Create your views here.
User=get_user_model()
from ComptesSmart.models import *


def genererCodeParrainage(longueur=15):
    caracteres = string.ascii_uppercase + string.digits + '_'
    code = ''.join(random.choice(caracteres) for _ in range(longueur))
    return code

# Create your views here.

############################## AUTHENTIFICATION ##############################
##############################################################################
def inscription(request):
    
    if request.method == 'POST':
        # traiter le formulaire
        passwordConfirm =request.POST.get("passwordConf")
        password =request.POST.get("password")
        name =request.POST.get("nom")
        telephone=request.POST.get("telephone")
        telephone2=request.POST.get("telephone2")
        Remember=request.POST.get("remember-me")
        codeParrain=request.POST.get("codeParrain")
        codeParrainage=genererCodeParrainage()
        
        historique_solde="0|"+datetime.date.today().strftime("%d-%m-%Y")+"#"
        print(f"REMEMBER : {Remember}")
        if codeParrain !="" and codeParrainage !=None:
            parrain=get_object_or_404(Utilisateur,codeParrainage=codeParrain)
        else:
            parrain=None
        
        if password==passwordConfirm:
            try:
              if parrain:
                  if telephone2!="" :
                    
                    user=User.objects.create_user(username=telephone,nom=name,password=password,parrain=parrain,telephone2=telephone2,codeParrainage=codeParrainage,historique_solde=historique_solde) # type: ignore
                  else:
                    user=User.objects.create_user(username=telephone,nom=name,password=password,parrain=parrain,codeParrainage=codeParrainage,historique_solde=historique_solde) # type: ignore
                      
              else:
                if telephone2!="" :
                    
                    user=User.objects.create_user(username=telephone,nom=name,password=password,telephone2=telephone2,codeParrainage=codeParrainage,historique_solde=historique_solde) # type: ignore
                else:
                    user=User.objects.create_user(username=telephone,nom=name,password=password,codeParrainage=codeParrainage,historique_solde=historique_solde) # type: ignore
                      
              login(request,user)
              #request.session.set_expiry(1209600) # 2 weeks
              if  Remember==False:
                  
                print("not remember")

               # request.session.set_expiry(0)
            except Exception as e:
                print(f"L'ERREUR EST : {e} ")
                return JsonResponse({"success": False, "message": " l'utilisateur existe deja."}) # Renvoyer une réponse JSON avec un indicateur d'échec et un message d'erreur

            
        #apres inscription on le redirige
            return JsonResponse({"success": True, "redirect_url": "/"}) # Renvoyer une réponse JSON avec un indicateur de succès et l'URL de redirection
        else:
            return JsonResponse({"success": False, "message": "Les mots de passe ne correspondent pas."}) # Renvoyer une réponse JSON avec un indicateur d'échec et un message d'erreur
    else :
        return render(request,"ComptesSmart/signup.html")

def inscriptionParrainee(request,code):
    
    return render(request,'ComptesSmart/signup.html',context={'code':code})

def connexion(request):
    if request.method == 'POST':
        # conecter l'utilisateur
        telephone = request.POST.get("telephone")
        print(telephone + " est le telephone")
        password =request.POST.get("password")
        Remember =request.POST.get("remember-me")
        print("le mdp est : "+password)
        
        user=authenticate(username=telephone, password=password) 
        if user:
            
            login(request,user)
            request.session.set_expiry(1209600) # 2 weeks
            if not Remember:
                print("ok")
                request.session.set_expiry(0)
            return JsonResponse({"success": True, "redirect_url": "/"})#apres inscription on le redirige
        else:    
            return JsonResponse({"success": False, "message": "Nom d'utilisateur ou mot de passe incorrect !"}) # Renvoyer une réponse JSON avec un indicateur d'échec et un message d'erreur

    else :
        return render(request,'ComptesSmart/signin.html')


def deconnexion(request):
    logout(request)
    return render(request,'ComptesSmart/signin.html')

############################## AUTHENTIFICATION ##############################
##############################################################################