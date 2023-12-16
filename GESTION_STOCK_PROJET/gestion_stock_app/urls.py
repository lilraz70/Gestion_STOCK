from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    
    path('category', create_category, name='category'),
    path('liste_categories/', liste_categories, name='liste_categories'),
    path('update_category/<int:id>', update_category, name='update_category'),
    path('delete_category/<int:id>', delete_category, name='delete_category'),


    path('enregistrement_produit_entrant/', enregistrement_produit_entrant, name='enregistrement_produit_entrant'),
    path('liste_produits_entrants/', liste_produits_entrants, name='liste_produits_entrants'),
    path('modifier_produit_entrant/<int:id>', modifier_produit_entrant, name='modifier_produit_entrant'),
    path('supprimer_produit_entrant/<int:id>', supprimer_produit_entrant, name='supprimer_produit_entrant'),

    
    path('liste_produits_sortants/', liste_produits_sortants, name='liste_produits_sortants'),
    path('enregistrement_produit_sortant/', enregistrement_produit_sortant, name='enregistrement_produit_sortant'),
    path('modifier_produit_sortant/<int:id>', modifier_produit_sortant, name='modifier_produit_sortant'),
    path('supprimer_produit_sortant/<int:id>', supprimer_produit_sortant, name='supprimer_produit_sortant'),
    
    path('liste_produits_sortants_grossiste/', liste_produits_sortants_grossiste, name='liste_produits_sortants_grossiste'),
    path('enregistrement_produit_sortant_grossiste/', enregistrement_produit_sortant_grossiste, name='enregistrement_produit_sortant_grossiste'),
    path('modifier_produit_sortant_grossiste/<int:id>', modifier_produit_sortant_grossiste, name='modifier_produit_sortant_grossiste'),
    path('supprimer_produit_sortant_grossiste/<int:id>', supprimer_produit_sortant_grossiste, name='supprimer_produit_sortant_grossiste'),



    path('liste_produits/', liste_produits, name='liste_produits'),
    path('ajouter_produits/', ajouter_produit, name='ajouter_produits'),
    path('modifier_produits/<int:pk>', modifier_produit, name='modifier_produits'),
    path('supprimer_produits/<int:pk>', supprimer_produit, name='supprimer_produits'),


    






]