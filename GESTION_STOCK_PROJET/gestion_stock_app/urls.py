from django.conf import settings
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('historique', historique, name='historique'),

    path('category', create_category, name='category'),
    path('liste_categories/', liste_categories, name='liste_categories'),
    path('update_category/<id>', update_category, name='update_category'),
    path('delete_category/<id>', delete_category, name='delete_category'),
    path('create_category/', create_category, name='create_category'),

    path('enregistrement_produit_entrant/', enregistrement_produit_entrant, name='enregistrement_produit_entrant'),
    path('liste_produits_entrants/', liste_produits_entrants, name='liste_produits_entrants'),
    path('modifier_produit_entrant/<id>', modifier_produit_entrant, name='modifier_produit_entrant'),
    path('supprimer_produit_entrant/<id>', supprimer_produit_entrant, name='supprimer_produit_entrant'),

    path('stocks/', liste_stocks, name="stocks"),
    path('ajouter_stock/', ajouter_stock, name='ajouter_stock'),
    path('modifier_stock/<stock_id>', modifier_stock, name='modifier_stock'),

    path('liste_produits_sortants/', liste_produits_sortants, name='liste_produits_sortants'),
    path('enregistrement_produit_sortant/', enregistrement_produit_sortant, name='enregistrement_produit_sortant'),
    path('modifier_produit_sortant/<id>', modifier_produit_sortant, name='modifier_produit_sortant'),
    path('supprimer_produit_sortant/<id>', supprimer_produit_sortant, name='supprimer_produit_sortant'),

    path('liste_produits_sortants_grossistes/', liste_produits_sortants_grossiste, name='liste_produits_sortants_grossiste'),
    path('enregistrement_produit_sortant_grossiste/', enregistrement_produit_sortant_grossiste, name='enregistrement_produit_sortant_grossiste'),
    path('modifier_produit_sortant_grossiste/<id>', modifier_produit_sortant_grossiste, name='modifier_produit_sortant_grossiste'),
    path('supprimer_produit_sortant_grossiste/<id>', supprimer_produit_sortant_grossiste, name='supprimer_produit_sortant_grossiste'),

    path('listes_produits/', liste_produits, name='liste_produits'),
    path('ajouter_produits/', ajouter_produit, name='ajouter_produits'),
    path('modifier_produits/<id>', modifier_produit, name='modifier_produits'),
    path('supprimer_produits/<id>', supprimer_produit, name='supprimer_produits'),

    path('fournisseurs/', fournisseur, name="fournisseurs"),
    path("addFournisseur/", fournisseur, name="addFournisseur"),
    path("editFournisseur/<id>", fournisseur, name="editFournisseur"),
    path("deleteFournisseur/<id>", fournisseur, name="deleteFournisseur"),
    
    path('liste-clients/', client, name="clients"),
    path('addClient/', client, name="addClient"),
    path('editClient/<id>', client, name="editClient"),
    path('deleteClient/<id>', client, name="deleteClient"),
    
    path('liste-grossistes/', grossiste, name="grossistes"),
    path('addGrossiste/', grossiste, name="addGrossiste"),
    path('editGrossiste/<id>', grossiste, name="editGrossiste"),
    path('deleteGrossiste/<id>', grossiste, name="deleteGrossiste"),

    path('notifications/', alert, name="notifications"),
    path('alerts', hist_alert, name="alerts")

]