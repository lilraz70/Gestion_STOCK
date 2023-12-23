from django.shortcuts import get_object_or_404, render,redirect
from .models import Fournisseur, Grossiste, Client, Categories_Produit, Produit, Stock, Sortie_grossiste, Sortie_client, Entrer
from .forms import *

def fournisseur(request):
  fournisseurs = Fournisseur.objects.all()
  return render(request,'acteurs.html',{'acteurs':fournisseurs})

def grossiste(request):
  fournisseurs = Grossiste.objects.all()
  return render(request,'acteurs.html',{'acteurs':fournisseurs})

def client(request):
  clients = Client.objects.all()
  return render(request,'acteurs.html',{'acteurs':clients})

def alert(request):
    stocks = Stock.objects.all()
    for stock in stocks:
        if stock.total_produit_restants <= stock.seuil_alerte_produit and stock.alerte == False:
            Stock.objects.filter(id = stock.id).update(alerte = True)
        if stock.total_produit_restants > stock.seuil_alerte_produit and stock.alerte == True:
            Stock.objects.filter(id = stock.id).update(alerte = False)
    seuil_stock = Stock.objects.filter(alerte=True)
    notification = [f"Seuil de {produit.produit.nom_produit} arriver" for produit in seuil_stock]
    return render(request,"_partiel/_notifications.html",{"notifications": notification})

def dashboard(request):
    
    produits_entrants = Entrer.objects.all()
    nombre_total_produits_entrants = produits_entrants.count()
    produits_sortants_client = Sortie_client.objects.all()
    nombre_produits_sortants_client = produits_sortants_client.count()
    produits = Produit.objects.all()
    nombre_total_produits = produits.count()
    stock = Stock.objects.all() 
    nombre_total_stock = produits.count()
    historique_entries = Historique.objects.all().order_by('-date')[:5]  
    stocks = Stock.objects.all()


    
    context = {
            'produits_entrants': produits_entrants,
            'nombre_total_produits_entrants': nombre_total_produits_entrants,
            'produits_sortants_client':produits_sortants_client,
            'nombre_produits_sortants_client':nombre_produits_sortants_client,
            'produits':produits,
            'nombre_total_produits':nombre_total_produits,
            'stock':stock,
            'nombre_total_stock':nombre_total_stock,
            'historique_entries': historique_entries,
            'stocks': stocks,
            
            
        }    
    return render(request,'dashboard.html',context)

def historique(request):
    historique_entries = Historique.objects.all().order_by('-date')[:20]  

    context = {
        'historique_entries': historique_entries,
    }

    return render(request, 'historique.html', context)

#les vues pour les stocks
def liste_stocks(request):
    stocks = Stock.objects.all()

    context = {
        'stocks': stocks,
    }

    return render(request, 'stocks.html', context)

def ajouter_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stocks')
    else:
        form = StockForm()
    return render(request, 'ajouter_stock.html', {'form': form})

def modifier_stock(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('stocks')
    else:
        form = StockForm(instance=stock)
    return render(request, 'modifier_stock.html', {'form': form, 'stock': stock})

def supprimer_stock(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    stock.delete()
    return redirect('stocks')

#les vues des catégories
def liste_categories(request):
    categories = Categories_Produit.objects.all()
    for category in categories:
        category.update_nombre_produit()
        category.save()
    categories = Categories_Produit.objects.all()
    return render(request, 'liste_categories.html', {'categories': categories})

def create_category(request):
    if request.method == 'POST':
        form = CategoriesProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')  
    else:
        form = CategoriesProduitForm()

    return render(request, 'create_category.html', {'form': form})

def update_category(request, id):
    category = get_object_or_404(Categories_Produit, id=id)

    if request.method == 'POST':
        form = CategoriesProduitForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')  
    else:
        form = CategoriesProduitForm(instance=category)

    return render(request, 'create_category.html', {'form': form, 'category': category})

def delete_category(request, id):
    category = get_object_or_404(Categories_Produit, id=id)
    category.delete()
    return redirect('liste_categories')

#les vues des produits entrants
def enregistrement_produit_entrant(request):
    form = EntrerProduitForm()
    if request.method == 'POST':
        form = EntrerProduitForm(request.POST)
        if form.is_valid():
            entrer_produit = form.save(commit=False)
            entrer_produit.update_prix_total()  
            entrer_produit.save()
            return redirect('liste_produits_entrants')  
        form = EntrerProduitForm()

    return render(request, 'enregistrement_produit_entrant.html', {'form': form})

def liste_produits_entrants(request):
    produits_entrants = Entrer.objects.all()
    nombre_total_produits_entrants = produits_entrants.count()

    context = {
        'produits_entrants': produits_entrants,
        'nombre_total_produits_entrants': nombre_total_produits_entrants,
    }

    return render(request, 'liste_produits_entrants.html', context)

def modifier_produit_entrant(request, id):
    entrer_produit = get_object_or_404(Entrer, id=id)

    if request.method == 'POST':
        form = EntrerProduitForm(request.POST, instance=entrer_produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits_entrants')
    else:
        form = EntrerProduitForm(instance=entrer_produit)

    return render(request, 'enregistrement_produit_entrant.html', {'form': form, 'entrer_produit': entrer_produit})

def supprimer_produit_entrant(request, id):
    entrer_produit = get_object_or_404(Entrer, id=id)

    if request.method == 'POST':
        entrer_produit.delete()
        return redirect('liste_produits_entrants')

    return render(request, 'enregistrement_produit_entrant.html', {'entrer_produit': entrer_produit})

#les vues des produits sortants clients
def liste_produits_sortants(request):
    sortants_clients = Sortie_client.objects.all()
    nombre_total_sortants_clients = sortants_clients.count()

    context = {
        'sortants_clients': sortants_clients,
        'nombre_total_sortants_clients': nombre_total_sortants_clients,
    }

    return render(request, 'liste_produits_sortants.html', context)

def enregistrement_produit_sortant(request):
    form = SortantClientForm()
    if request.method == 'POST':
        form = SortantClientForm(request.POST)
        if form.is_valid():
            entrer_produit = form.save(commit=False)
            entrer_produit.update_prix_total()  
            entrer_produit.save()
            return redirect('liste_produits_sortants')  
    else:
        form = SortantClientForm()

    return render(request, 'enregistrement_produit_sortant.html', {'form': form})

def modifier_produit_sortant(request, id):
    sortie_client_produit = get_object_or_404(Sortie_client, id=id)

    if request.method == 'POST':
        form = SortantClientForm(request.POST, instance=sortie_client_produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits_sortants')
    else:
        form = SortantClientForm(instance=sortie_client_produit)

    return render(request, 'enregistrement_produit_sortant.html', {'form': form, 'sortie_client_produit': sortie_client_produit})

def supprimer_produit_sortant(request, id):
    sortie_client_produit = get_object_or_404(Sortie_client, id=id)

    if request.method == 'POST':
        sortie_client_produit.delete()
        return redirect('liste_produits_sortants')

    return render(request, 'enregistrement_produit_sortant.html', {'sortie_client_produit': sortie_client_produit})

#les vues des produits sortants grossistes
def liste_produits_sortants_grossiste(request):
    sortants_clients = Sortie_grossiste.objects.all()
    nombre_total_sortants_clients = sortants_clients.count()

    context = {
        'sortants_clients': sortants_clients,
        'nombre_total_sortants_clients': nombre_total_sortants_clients,
    }

    return render(request, 'liste_produits_sortants_grossiste.html', context)

def enregistrement_produit_sortant_grossiste(request):
    form = SortantGrossisteForm()
    if request.method == 'POST':
        form = SortantGrossisteForm(request.POST)
        if form.is_valid():
            entrer_produit = form.save(commit=False)
            entrer_produit.update_prix_total()  
            entrer_produit.save()
            return redirect('liste_produits_sortants_grossiste')  
    else:
        form = SortantGrossisteForm()

    return render(request, 'enregistrement_produit_sortant_grossiste.html', {'form': form})

def modifier_produit_sortant_grossiste(request, id):
    sortie_grossiste_produit = get_object_or_404(Sortie_grossiste, id=id)

    if request.method == 'POST':
        form = SortantGrossisteForm(request.POST, instance=sortie_grossiste_produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits_sortants')
    else:
        form = SortantGrossisteForm(instance=sortie_grossiste_produit)

    return render(request, 'enregistrement_produit_sortant.html', {'form': form, 'sortie_grossiste_produit': sortie_grossiste_produit})

def supprimer_produit_sortant_grossiste(request, id):
    sortie_client_produit = get_object_or_404(Sortie_grossiste, id=id)

    if request.method == 'POST':
        sortie_client_produit.delete()
        return redirect('liste_produits_sortants_grossiste')

    return render(request, 'enregistrement_produit_sortant_grossiste.html', {'sortie_client_produit': sortie_client_produit})

#les vues des produits 
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'liste_produits.html', {'produits': produits})

def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')  
    else:
        form = ProduitForm()

    return render(request, 'ajouter_produit.html', {'form': form})

def modifier_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)

    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')  
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'ajouter_produit.html', {'form': form, 'produit': produit})

def supprimer_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)

    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')  

    return render(request, 'ajouter_produit.html', {'produit': produit})
