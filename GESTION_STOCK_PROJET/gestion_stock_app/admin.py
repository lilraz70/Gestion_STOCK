from django.contrib import admin
from .models import Fournisseur, Grossiste, Client, Categories_Produit, Produit, Stock, Sortie_grossiste, Sortie_client, Entrer, Historique

# Register your models here.
admin.site.register(Fournisseur)
admin.site.register(Grossiste)
admin.site.register(Client)
admin.site.register(Categories_Produit)
admin.site.register(Produit)
admin.site.register(Sortie_client)
admin.site.register(Sortie_grossiste)
admin.site.register(Stock)
admin.site.register(Entrer)
admin.site.register(Historique)