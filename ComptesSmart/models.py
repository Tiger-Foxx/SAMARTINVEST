from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models



class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, telephone, **extra_fields):
        if not telephone:
            raise ValueError('Le numéro de téléphone doit être défini')
        user = self.model(telephone=telephone, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(telephone, password, **extra_fields)

class Utilisateur(AbstractUser):
    username = models.CharField(max_length=13, unique=True)
    email = models.EmailField(null=True,blank=True)
    
    password = models.CharField(max_length=500)
    nom=models.CharField(max_length=200)
    ville=models.CharField(max_length=100,null=True,blank=True)
    telephone2 = models.CharField(max_length=13,null=True,blank=True)
    
    #champs non editables
    date=models.DateField(auto_now=True,editable=False)
    date_contrat=models.DateField(null=True,blank=True)
    is_parain = models.BooleanField(default=False,null=True,blank=True)
    codeParrainage=models.CharField(max_length=200,null=True,blank=True)
    solde=models.FloatField(null=True, blank=True,default=0)
    contrat_courant=models.ForeignKey("SmartInvestApp.Contrat",null=True, blank=True,on_delete=models.SET_NULL)
    historique_solde=models.TextField(default="")
    parrain = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False)
    contrat_expire=models.BooleanField(default=False)
    def __str__(self):
        return f"Utilisateur | nom: {self.nom} | telphone: {self.username}"

