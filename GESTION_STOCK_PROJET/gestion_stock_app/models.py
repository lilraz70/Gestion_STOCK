from django.db import models

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

