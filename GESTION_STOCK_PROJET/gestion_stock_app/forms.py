from django import forms
from .models import *

class CategoriesProduitForm(forms.ModelForm):
    class Meta:
        model = Categories_Produit
        fields = ['nom_categorie', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 5}),  
        }
        
class EntrerProduitForm(forms.ModelForm):
    class Meta:
        model = Entrer
        fields = ['produit', 'fournisseur', 'quantite']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantite'].widget.attrs.update({'class': 'form-control', 'min': 1})


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom_produit', 'description', 'categorie', 'prix_en_gros', 'prix_details', 'prix_fournisseur']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                 
            
class SortantClientForm(forms.ModelForm):
    class Meta:
        model = Sortie_client
        fields = ['produit','client', 'quantite', 'prix_total']

class SortantGrossisteForm(forms.ModelForm):
    class Meta:
        model = Sortie_grossiste
        fields = ['produit','grossiste', 'quantite', 'prix_total']

    