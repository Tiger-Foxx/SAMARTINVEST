################################### UTILITAIRES #####################################################
################################### UTILITAIRES #####################################################
################################### UTILITAIRES #####################################################

import datetime
import random
import string
from ComptesSmart.models import Utilisateur
from SmartInvestApp.models import Notification, Transaction


def trouver_contrat_suivant(contrats, contrat_courant):
    # Trier les contrats par montant en ordre croissant
    contrats_tries = sorted(contrats, key=lambda c: c.Montant)
    if contrat_courant:
        
        # Trouver l'index du contrat courant
        index_courant = contrats_tries.index(contrat_courant)
        # Vérifier s'il existe un contrat suivant
        if index_courant < len(contrats_tries) - 1:
            return contrats_tries[index_courant + 1]
        else:
            # Retourner None si le contrat courant est le dernier
            return None
    else :
        return  contrats_tries[0]

def genererCodeParrainage(longueur=15):
    caracteres = string.ascii_uppercase + string.digits + '_'
    code = ''.join(random.choice(caracteres) for _ in range(longueur))
    return code

def recuperer_transactions_utilisateur(username,nombre_max=15):
    # Récupération de l'utilisateur par son username
    utilisateur = Utilisateur.objects.get(username=username)
    
    # Récupération de toutes les transactions de l'utilisateur
    transactions = Transaction.objects.filter(Auteur=utilisateur,valide=True).order_by('-date')[:nombre_max]
    
    # Création des listes pour les montants, dates et types
    montants = [transaction.Montant for transaction in transactions]
    dates = [transaction.date.strftime("%d/%m/%Y") for transaction in transactions]
    types = [transaction.Type for transaction in transactions]
    
    return montants, dates, types
def extraire_informations_historique(historique_solde, nombre_max=15):
    liste_montants = []
    liste_dates = []
    # Séparer chaque entrée de l'historique et inverser l'ordre pour obtenir les plus récents
    entrees_historique = historique_solde.strip('#').split('#')[-nombre_max:]
    for entree in entrees_historique:
        if entree:  # Vérifier si l'entrée n'est pas vide
            montant, date = entree.split('|')
            liste_montants.append(float(montant))
            liste_dates.append(date)
    return liste_montants, liste_dates




from django.utils import timezone
from datetime import timedelta

def creer_notification(texte_motif):
    # Création d'une nouvelle instance de Notification
    nouvelle_notification = Notification(Motif=texte_motif)
    # Enregistrement de la nouvelle notification dans la base de données
    nouvelle_notification.save()
    return nouvelle_notification


def recompenserParrains(utilisateur, n):
    # Convertir le pourcentage 'n' en un nombre décimal
    pourcentage_n = float(n) / 100

    # Vérifier si l'utilisateur a un parrain
    if utilisateur.parrain:
        # Calculer la récompense pour le parrain
        recompense_parrain = (utilisateur.contrat_courant.Montant * utilisateur.contrat_courant.pourcentage / 100) * pourcentage_n
        # Augmenter le solde du parrain
        utilisateur.parrain.solde += recompense_parrain
        ajout_historique=str(utilisateur.parrain.solde)+"|"+datetime.date.today().strftime("%d-%m-%Y")+"#"
        utilisateur.parrain.historique_solde+=ajout_historique
        utilisateur.parrain.save()

        # Vérifier si le parrain a aussi un parrain (grand-parrain)
        if utilisateur.parrain.parrain:
            # Calculer la récompense pour le grand-parrain
            recompense_grand_parrain = recompense_parrain * 0.04
            # Augmenter le solde du grand-parrain
            utilisateur.parrain.parrain.solde += recompense_grand_parrain
            ajout_historique=str(utilisateur.parrain.parrain.solde)+"|"+datetime.date.today().strftime("%d-%m-%Y")+"#"
            utilisateur.parrain.parrain.historique_solde+=ajout_historique
            utilisateur.parrain.parrain.save()

# Exemple d'utilisation de la fonction
# recompenserParrains(instance_de_utilisateur, 8)
def distribuerGains(pourcentage=3.5, jours=0, montant_minimum=0):
    try:
        pourcentage = float(pourcentage.replace(',', '.'))
        jours = int(jours)
        montant_minimum = float(montant_minimum.replace(',', '.'))
    except Exception as e:
        pass
    # Conversion des paramètres en nombres
    pourcentage = float(pourcentage)
    jours = int(jours)
    montant_minimum = float(montant_minimum)

    # Détermination de la date limite
    date_limite = timezone.now().date() - timedelta(days=jours)

    # Sélection des utilisateurs éligibles
    utilisateurs_eligibles = Utilisateur.objects.filter(
        date__lte=date_limite,
        contrat_courant__disponible=True,
        contrat_expire=False,
        contrat_courant__Montant__gte=montant_minimum
    )

    # Mise à jour du solde des utilisateurs éligibles et création de notifications
    for utilisateur in utilisateurs_eligibles:
        #verifier si c'est le premier contrat du user :
        if len(utilisateur.historique_solde.split("#"))<3:
            recompenserParrains(utilisateur, 8)
       
        montant_bonus = utilisateur.contrat_courant.Montant * pourcentage / 100
        utilisateur.solde += montant_bonus
        ajout_historique=str(utilisateur.solde)+"|"+datetime.date.today().strftime("%d-%m-%Y")+"#"
        utilisateur.historique_solde+=ajout_historique
        utilisateur.save()
        # Création de la notification
        texte_notif = f"LES GAINS ONT ETE REDISTRIBUES A TOUS LES UTILISATEURS "
        if montant_minimum >0:
            texte_notif+=F"TITULAIRES D'UN CONTRAT D'AU MOINS {montant_minimum} XAF"
        if jours > 0:
            texte_notif += f" ET PRESENTS DEPUIS AU MOINS {jours} JOURS."
        else:
            texte_notif += "."
        creer_notification(texte_notif)
        
      
      
def Verifier():
    utilisateurs = Utilisateur.objects.filter(contrat_courant__isnull=False, contrat_expire=False)
    for utilisateur in utilisateurs:
        utilisateur.verifier_expiration_contrat()
  




################################### UTILITAIRES #####################################################
################################### UTILITAIRES #####################################################
################################### UTILITAIRES #####################################################