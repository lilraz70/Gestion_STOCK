from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Categories_Produit(models.Model):

    nom_categorie = models.CharField( max_length=150)
    description = models.TextField()
    total_produits = models.IntegerField()

    class Meta:
        verbose_name = ("Categories_Produit")
        verbose_name_plural = ("Categories_Produits")

    def __str__(self):
        return self.nom_categorie
    
    def update_nombre_produit(self):
        self.total_produits = Produit.objects.filter(categorie = self ).count()


class Produit(models.Model):

    nom_produit = models.CharField( max_length=150)
    description = models.TextField()
    categorie = models.ForeignKey( Categories_Produit, on_delete=models.SET_NULL, null=True )
    prix_en_gros = models.FloatField()
    prix_details = models.FloatField()
    prix = models.FloatField()

    class Meta:
        verbose_name = ("Produit")
        verbose_name_plural = ("Produits")

    def __str__(self):
        return self.nom_produit

@receiver(post_save,sender=Produit)
def set_nombre_produit(sender, instance, **kwargs):
    categorie = Categories_Produit.objects.get(pk = instance.categorie.pk) 
    categorie.update_nombre_produit()
    
class Stock(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL)
    total_produit_initial = models.IntegerField()
    total_produit_final = models.IntegerField()
    

    class Meta:
        verbose_name = ("Stock")
        verbose_name_plural = ("Stocks")

    def __str__(self):
        return self.name


