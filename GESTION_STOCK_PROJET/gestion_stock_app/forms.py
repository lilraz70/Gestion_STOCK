from django import forms
from .models import *

class CategoriesProduitForm(forms.ModelForm):
    class Meta:
        model = Categories_Produit
        fields = ['nom_categorie', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 5}),  
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
class EntrerProduitForm(forms.ModelForm):
    class Meta:
        model = Entrer
        fields = ['produit', 'fournisseur', 'quantite']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom_produit', 'description', 'categorie', 'prix_en_gros', 'prix_details', 'prix_fournisseur']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
                 
            
class SortantClientForm(forms.ModelForm):
    class Meta:
        model = Sortie_client
        fields = ['produit','client', 'quantite', ]
        widget = {
            'quantite': forms.IntegerField(validators=[
            MaxValueValidator(1000),
            MinValueValidator(1)
            ])
                                           
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
class SortantGrossisteForm(forms.ModelForm):
    class Meta:
        model = Sortie_grossiste
        fields = ['produit','grossiste', 'quantite',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('produit', 'total_produit',  'seuil_alerte_produit', )  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})