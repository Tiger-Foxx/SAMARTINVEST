from django.db import models



# Create your models here.
class Message(models.Model):
    date=models.DateField(auto_now=True,editable=False)
    title=models.CharField(max_length=128)
    image=models.ImageField(blank=True,upload_to='imagesMessages',null=True)
    contenu=models.TextField()
    NomAuteur=models.CharField(max_length=128,default="SMARTINVEST")    
    def __str__(self):
        return f"MESSAGE DE : {self.NomAuteur} LE {self.date}"
    

class Transaction(models.Model):
    from ComptesSmart.models import Utilisateur
    id=models.IntegerField(auto_created=True, primary_key=True,editable=False)
    date=models.DateTimeField(auto_now=True,editable=False)
    Numero=models.CharField(max_length=13,null=True,blank=True)
    PorteFeuille=models.CharField(max_length=100,null=True,blank=True)
    Montant=models.FloatField()
    contrat=models.FloatField(null=True, blank=True)
    MontantUSDT=models.FloatField(null=True, blank=True)
    Auteur=models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    Type=models.CharField(max_length=10)  
    valide=models.BooleanField(default=False)
    en_attente=models.BooleanField(default=True)
    def valider_transaction(self):
        self.valide = True
        self.en_attente = False
        self.save()

    def refuser_transaction(self):
        self.valide = False
        self.en_attente = False
        self.save()
    def __str__(self):
        if self.MontantUSDT:
            return f"{self.Type} DE : {self.Auteur.nom} LE {self.date} : {self.MontantUSDT} USDT"
        return f"{self.Type} DE : {self.Auteur.nom} LE {self.date} : {self.Montant} XAF"
    

class Contrat(models.Model):
    id=models.IntegerField(auto_created=True, primary_key=True,editable=False)
    Montant=models.FloatField()
    disponible=models.BooleanField(default=True)
    
    pourcentage=models.FloatField(default=3.5)
    def __str__(self):
        return f"CONTRAT {self.id} DE {self.Montant} DISPONIBLE"
    

class Notification(models.Model):
    id=models.IntegerField(auto_created=True, primary_key=True,editable=False)
    Motif=models.TextField()
    date=models.DateField(auto_now=True,editable=False)
    def __str__(self):
        return f"NOTIFICATION {self.id} LE {self.date} "
    

class Information(models.Model):
    OM=models.CharField(max_length=130,null=True,blank=True)
    nomOM=models.CharField(max_length=130,null=True,blank=True)
    MTN=models.CharField(max_length=13,null=True,blank=True)
    nomMTN=models.CharField(max_length=13,null=True,blank=True)
    
    BEP20=models.CharField(max_length=130,null=True,blank=True)
    ERC20=models.CharField(max_length=130,null=True,blank=True)
    TRC20=models.CharField(max_length=130,null=True,blank=True)
    prixUSDT=models.FloatField(default=606.37)

    def __str__(self):
        return f"VOS INFORMATIONS "
    