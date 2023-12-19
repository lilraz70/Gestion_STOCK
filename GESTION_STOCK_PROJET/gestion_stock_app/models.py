from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

########################################################
#                 Creaion de models                    #
########################################################

class Fournisseur(models.Model):

    nom_et_prenom = models.CharField( max_length=150, blank=True)
    nom_societe = models.CharField( max_length=50, blank=True)
    numero = models.CharField(max_length=50)
    autre_information = models.TextField(blank=True)

    class Meta:
        verbose_name = ("fournisseur")
        verbose_name_plural = ("fournisseurs")

    def __str__(self):
        return self.nom_societe + " - " + self.nom_et_prenom


class Grossiste(models.Model):

    nom_et_prenom = models.CharField( max_length=150)
    nom_societe = models.CharField( max_length=50, blank=True)
    numero = models.CharField(max_length=50)
    autre_information = models.TextField(blank=True)

    class Meta:
        verbose_name = ("grossiste")
        verbose_name_plural = ("grossistes")

    def __str__(self):
        return self.nom_societe + " - " + self.nom_et_prenom
   
class Client(models.Model):

    nom_et_prenom = models.CharField( max_length=150)
    numero = models.CharField(max_length=50)
    autre_information = models.TextField(blank=True)

    class Meta:
        verbose_name = ("Client")
        verbose_name_plural = ("Clients")

    def __str__(self):
        return self.nom_et_prenom 

class Categories_Produit(models.Model):

    nom_categorie = models.CharField( max_length=150)
    description = models.TextField(blank=True)
    total_produits = models.IntegerField(default=0, blank=True)

    class Meta:
        verbose_name = ("Categorie de Produit")
        verbose_name_plural = ("Categories de  Produits")

    def __str__(self):
        return self.nom_categorie
    
    def update_nombre_produit(self): #ici je met a jour le nombre de produits par categorie
        self.total_produits = Produit.objects.filter(categorie_id = self.pk ).count()
    
    def stock(self):
        produits = Produit.objects.filter(categorie=self)
        results = 0
        for produit in produits:
            results = results + Stock.objects.filter(produit=produit).first().total_produit_restants if Stock.objects.filter(produit=produit).count() != 0 else 0
            
        return results


class Produit(models.Model):

    nom_produit = models.CharField( max_length=150)
    description = models.TextField(blank=True)
    categorie = models.ForeignKey( Categories_Produit, on_delete=models.SET_NULL, null=True )
    prix_en_gros = models.FloatField()
    prix_details = models.FloatField()
    prix_fournisseur = models.FloatField()

    class Meta:
        verbose_name = ("Produit")
        verbose_name_plural = ("Produits")

    def __str__(self):
        return self.nom_produit

class Stock(models.Model):
    
    produit = models.OneToOneField(Produit, on_delete=models.CASCADE, null = True)
    total_produit = models.IntegerField(blank=True, default=0)
    total_produit_restants = models.IntegerField( blank=True, default=0)
    total_produit_sortis = models.IntegerField( blank=True, default=0)
    total_produit_entrant = models.IntegerField( blank=True, default=0)
    seuil_alerte_produit = models.IntegerField(default=5)
    alerte = models.BooleanField(default=False, blank=True)
    
    def save(self, *args, **kwargs):
        # Si c'est un nouvel objet, initialise le stock
        if not self.pk:
            self.initalisation_stock()
        else:
            if self.total_produit_restants <= self.seuil_alerte_produit:
                self.seuil_alerte_produit = True
        super().save(*args, **kwargs)
    
    def initalisation_stock(self):
        self.total_produit_restants = self.total_produit
    
    def update_sorti(self, sorti):
        self.total_produit_sortis = self.total_produit_sortis + sorti.quantite
        self.total_produit_restants = self.total_produit_restants - sorti.quantite
    
    def update_entrer(self, entrer):
        self.total_produit_entrant = self.total_produit_entrant + entrer.quantite
        self.total_produit = self.total_produit + entrer.quantite
        self.total_produit_restants = self.total_produit_restants + entrer.quantite

    
    
    class Meta:
        verbose_name = ("Stock")
        verbose_name_plural = ("Stocks")

    def __str__(self):
        return self.produit.nom_produit
    
class Sortie_grossiste(models.Model):
    
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null = True)
    grossiste = models.ForeignKey(Grossiste, on_delete=models.SET_NULL, null = True)
    quantite = models.IntegerField()
    prix_total = models.FloatField(blank=True)    
    
    class Meta:
        verbose_name = ("Sortie de grossiste")
        verbose_name_plural = ("Sortie de grossistes")
        
    def save(self, *args, **kwargs):
        # Si c'est un nouvel objet, initialise le stock
        if not self.pk:
            self.update_prix_total()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.produit.nom_produit + " - " + self.grossiste.nom_et_prenom
    
    def update_prix_total(self):
        self.prix_total = self.quantite*self.produit.prix_en_gros
    

class Sortie_client(models.Model):
    
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null = True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null = True)
    quantite = models.IntegerField()
    prix_total = models.FloatField(blank=True)    
    
    class Meta:
        verbose_name = ("Sortie de client")
        verbose_name_plural = ("Sortie de clients")
    
    def save(self, *args, **kwargs):
        # Si c'est un nouvel objet, initialise le stock
        if not self.pk:
            self.update_prix_total()
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.produit.nom_produit + " - " + self.client.nom_et_prenom
    
    def update_prix_total(self):
        self.prix_total = self.quantite*self.produit.prix_details


class Entrer(models.Model):
    
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null = True)
    quantite = models.IntegerField()
    prix_total = models.FloatField(blank=True)
    
    def save(self, *args, **kwargs):
        # Si c'est un nouvel objet, initialise le stock
        if not self.pk:
            self.update_prix_total()
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.fournisseur.nom_et_prenom
    
    def update_prix_total(self):
        self.prix_total = self.quantite*self.produit.prix_fournisseur


class Historique(models.Model):
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.description
    


########################################################
#   les differentes fonction de triggers(declancheur)  #
########################################################

@receiver(post_save, sender=Produit)
def set_nombre_produit(sender, instance, **kwargs):
    #mis ajour des nombre de produits par categorie
    categorie = Categories_Produit.objects.get(pk = instance.categorie.pk) 
    categorie.update_nombre_produit()
    categorie.save()

@receiver(post_save, sender=Sortie_grossiste)
def trigger_grossiste(sender, instance, **kwargs):
    
    stock = Stock.objects.get(produit = instance.produit)
    stock.update_sorti(instance)
    stock.save()

@receiver(post_save, sender=Sortie_client)
def trigger_client(sender, instance, **kwargs):

    stock = Stock.objects.get(produit = instance.produit)
    stock.update_sorti(instance)
    stock.save()
    
    
@receiver(post_save, sender=Entrer)
def trigger_entrer(sender, instance, **kwargs):
 
    stock = Stock.objects.get(produit = instance.produit)
    stock.update_entrer(instance)
    stock.save()
    
################# Pour l'historique ###################

def log_mouvement(sender, instance, created, action):
    model_name = sender.__name__
    object = sender.__str__(instance)
    object_name = f"{model_name} {object} {instance.pk}"
    action_str = "Création" if created else "Mise à jour" if action == "save" else "Suppression"
    
    description = f"{action_str} de {object_name}"
    Historique.objects.create(description=description)

def enregistrement_dans_historique(model):
    @receiver(post_save, sender=model)
    def log_model_creation_update(sender, instance, created, **kwargs):
        log_mouvement(sender, instance, created, "save")

    @receiver(post_delete, sender=model)
    def log_model_deletion(sender, instance, **kwargs):
        log_mouvement(sender, instance, False, "delete")
        
enregistrement_dans_historique(Fournisseur)
enregistrement_dans_historique(Grossiste)
enregistrement_dans_historique(Client)
enregistrement_dans_historique(Sortie_client)
enregistrement_dans_historique(Sortie_grossiste)
enregistrement_dans_historique(Categories_Produit)
enregistrement_dans_historique(Produit)
enregistrement_dans_historique(Stock)
enregistrement_dans_historique(Entrer)