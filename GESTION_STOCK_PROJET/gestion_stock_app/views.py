from django.shortcuts import get_object_or_404, render,redirect
from .models import Fournisseur, Grossiste, Client, Categories_Produit, Produit, Stock, Sortie_grossiste, Sortie_client, Entrer, AlertHistorique
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime

def enregistrement_alert_log(seuils):
    for seuil in seuils:
        if  AlertHistorique.objects.filter(intituler = seuil.produit.nom_produit, date=seuil.date).count() == 0:
            hist = AlertHistorique.objects.create(intituler = seuil.produit.nom_produit, date = seuil.date)
            hist.save()
            
        #[f"Seuil de stock de {produit.produit.nom_produit} est atteint" for produit in seuil_stock if produit]
@login_required
def fournisseur(request, id=0):
    
    if 'editFournisseur' in request.path and id !=0:
        instance = get_object_or_404(Fournisseur, pk=id)
        if request.method == 'POST':
            form = FournisseurForm(request.POST, instance = instance)
            if form.is_valid():
                form.save()
                return redirect('fournisseurs')
            form = FournisseurForm(instance=instance)
            messages.warning(request, "Donnees Invalides")
            return render(request, 'ajouter_acteurs.html', {'form':form})
        form = FournisseurForm(instance=instance)
        return render(request, 'ajouter_acteurs.html', {'form':form})
    if 'deleteFournisseur' in request.path and id !=0:
        fournisseur = get_object_or_404(Fournisseur, pk=id)
        fournisseur.delete()
        return redirect('fournisseurs')
    if 'addFournisseur' in request.path:
        if request.method == 'POST':
            form = FournisseurForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('fournisseurs')
            form = FournisseurForm()
            messages.warning(request, "Donnees Invalides")
            return render(request, 'ajouter_acteurs.html', {'form':form})
        form = FournisseurForm()
        return render(request, 'ajouter_acteurs.html', {'form':form})
    fournisseurs = Fournisseur.objects.all()
    return render(request,'acteurs.html',{'acteurs':fournisseurs})

@login_required
def grossiste(request, id=0):

    if 'editGrossiste' in request.path and id !=0:
        instance = get_object_or_404(Grossiste, pk=id)
        if request.method == 'POST':
            form = GrossisteForm(request.POST, instance = instance)
            if form.is_valid():
                form.save()
                return redirect('grossistes')
            form = GrossisteForm(instance=instance)
            messages.warning(request, "Donnees Invalides")
            return render(request, 'ajouter_acteurs.html', {'form':form})
        form = GrossisteForm(instance=instance)
        return render(request, 'ajouter_acteurs.html', {'form':form})
    if 'deleteGrossiste' in request.path and id !=0:
        fournisseur = get_object_or_404(Grossiste, pk=id)
        fournisseur.delete()
        return redirect('fournisseurs')
    if 'addGrossiste' in request.path:
        if request.method == 'POST':
            form = GrossisteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('fournisseurs')
            form = GrossisteForm()
            messages.warning(request, "Donnees Invalides")
            return render(request, 'ajouter_acteurs.html', {'form':form})
        form = GrossisteForm()
        return render(request, 'ajouter_acteurs.html', {'form':form})
    fournisseurs = Grossiste.objects.all()
    return render(request,'acteurs.html',{'acteurs':fournisseurs})

@login_required
def client(request, id=0):
    if 'editClient' in request.path and id !=0:
        instance = get_object_or_404(Client, pk=id)
        if request.method == 'POST':
            form = ClientForm(request.POST, instance = instance)
            if form.is_valid():
                form.save()
                return redirect('clients')
            form = ClientForm(instance=instance)
            messages.warning(request, "Donnees Invalides")
            return render(request, 'ajouter_acteurs.html', {'form':form})
        form = ClientForm(instance=instance)
        return render(request, 'ajouter_acteurs.html', {'form':form})
    if 'deleteClient' in request.path and id !=0:
        fournisseur = get_object_or_404(Client, pk=id)
        fournisseur.delete()
        return redirect('clients')
    if 'addClient' in request.path:
        if request.method == 'POST':
            form = ClientForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('clients')
            form = ClientForm()
            messages.warning(request, "Donnees Invalides")
            return render(request, 'ajouter_acteurs.html', {'form':form})
        form = ClientForm()
        return render(request, 'ajouter_acteurs.html', {'form':form})
    clients = Client.objects.all()
    return render(request,'acteurs.html',{'acteurs':clients})

@login_required
def alert(request):
    stocks = Stock.objects.all()
    for stock in stocks:
        date_actu =datetime.datetime.now()
        if stock.total_produit_restants <= stock.seuil_alerte_produit and stock.alerte == False:
            Stock.objects.filter(id = stock.id).update(alerte = True, date=date_actu)
        if stock.total_produit_restants > stock.seuil_alerte_produit and stock.alerte == True:
            Stock.objects.filter(id = stock.id).update(alerte = False, date=None)
    seuil_stock = Stock.objects.filter(alerte=True)
    enregistrement_alert_log(seuil_stock)
    notifications = []
    index = 0
    for seuil in seuil_stock:
        if  AlertHistorique.objects.filter(intituler = seuil.produit.nom_produit, date=seuil.date).count() != 0 and seuil.total_produit_restants != 0 :
            notifications.append({
                'id': index,
                'intituler': f"Seuil de stock de '{seuil.produit.nom_produit}' est atteint",
                'date': seuil.date
                })
            index += 1
        if seuil.total_produit_restants == 0 :
            notifications.append({
                'id': index,
                'intituler': f"Seuil de stock de '{seuil.produit.nom_produit}' est a 0(Produits finis)",
                'date': seuil.date
                })
            index += 1
        
    total_notif = len(notifications)
    print(datetime.datetime.now())
    return render(request,"_partiel/_notifications.html",{"notifications": notifications, 'total_notif': total_notif})

@login_required
def hist_alert(request):
    historique_alerts = AlertHistorique.objects.all()
    return render(request,'alert.html',{'alerts':historique_alerts})

@login_required
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
@login_required
def historique(request):
    historique_entries = Historique.objects.all().order_by('-date')[:20]  

    context = {
        'historique_entries': historique_entries,
    }

    return render(request, 'historique.html', context)

#les vues pour les stocks
@login_required
def liste_stocks(request):
    stocks = Stock.objects.all()

    context = {
        'stocks': stocks,
    }

    return render(request, 'stocks.html', context)
@login_required
def ajouter_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('stocks')
    else:
        form = StockForm()
    return render(request, 'ajouter_stock.html', {'form': form})
@login_required
def modifier_stock(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('stocks')
    else:
        form = StockForm(instance=stock)
    return render(request, 'modifier_stock.html', {'form': form, 'stock': stock})
@login_required
def supprimer_stock(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    stock.delete()
    messages.success(request, "Operation reussit")
    next_param = request.GET.get('next', None)
    if next_param:
                return redirect(request.GET['next'])
    return redirect('stocks')

#les vues des catégories
@login_required
def liste_categories(request):
    categories = Categories_Produit.objects.all()
    for category in categories:
        category.update_nombre_produit()
        category.save()
    categories = Categories_Produit.objects.all()
    return render(request, 'liste_categories.html', {'categories': categories})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoriesProduitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('liste_categories')  
    else:
        form = CategoriesProduitForm()

    return render(request, 'ajouter_category.html', {'form': form})

@login_required
def update_category(request, id):
    category = get_object_or_404(Categories_Produit, id=id)

    if request.method == 'POST':
        form = CategoriesProduitForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('liste_categories')  
    else:
        form = CategoriesProduitForm(instance=category)

    return render(request, 'create_category.html', {'form': form, 'category': category})

@login_required
def delete_category(request, id):
    category = get_object_or_404(Categories_Produit, id=id)
    category.delete()
    messages.success(request, "Operation reussit")
    next_param = request.GET.get('next', None)
    if next_param:
                return redirect(request.GET['next'])
    return redirect('liste_categories')

#les vues des produits entrants
@login_required
def enregistrement_produit_entrant(request):
    form = EntrerProduitForm()
    if request.method == 'POST':
        form = EntrerProduitForm(request.POST)
        if form.is_valid():
            entrer_produit = form.save(commit=False)
            entrer_produit.update_prix_total()  
            entrer_produit.save()
            messages.success(request, "Operation reussit")
            return redirect('liste_produits_entrants')  
        form = EntrerProduitForm()

    return render(request, 'enregistrement_produit_entrant.html', {'form': form})

@login_required
def liste_produits_entrants(request):
    produits_entrants = Entrer.objects.all()
    nombre_total_produits_entrants = produits_entrants.count()

    context = {
        'produits_entrants': produits_entrants,
        'nombre_total_produits_entrants': nombre_total_produits_entrants,
    }

    return render(request, 'liste_produits_entrants.html', context)

@login_required
def modifier_produit_entrant(request, id):
    entrer_produit = get_object_or_404(Entrer, id=id)

    if request.method == 'POST':
        form = EntrerProduitForm(request.POST, instance=entrer_produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('liste_produits_entrants')
    else:
        form = EntrerProduitForm(instance=entrer_produit)

    return render(request, 'enregistrement_produit_entrant.html', {'form': form, 'entrer_produit': entrer_produit})

@login_required
def supprimer_produit_entrant(request, id):
    entrer_produit = get_object_or_404(Entrer, id=id)

    if request.method == 'POST':
        entrer_produit.delete()
        messages.success(request, "Operation reussit")
        next_param = request.GET.get('next', None)
        if next_param:
                return redirect(request.GET['next'])
        return redirect('liste_produits_entrants')

    return render(request, 'enregistrement_produit_entrant.html', {'entrer_produit': entrer_produit})

#les vues des produits sortants clients
@login_required
def liste_produits_sortants(request):
    sortants_clients = Sortie_client.objects.all()
    nombre_total_sortants_clients = sortants_clients.count()

    context = {
        'sortants_clients': sortants_clients,
        'nombre_total_sortants_clients': nombre_total_sortants_clients,
    }

    return render(request, 'liste_produits_sortants.html', context)

@login_required
def enregistrement_produit_sortant(request):
    form = SortantClientForm()
    if request.method == 'POST':
        form = SortantClientForm(request.POST)
        if form.is_valid():
            produit = request.POST['produit']
            quantite = int(request.POST['quantite'])
            if quantite > Stock.objects.filter(produit = produit).first().total_produit_restants:
                messages.warning(request, "La quantite que vous avez mis est superieur a celle du stock")
                return render(request, 'enregistrement_produit_sortant.html', {'form': form})
            entrer_produit = form.save(commit=False)
            entrer_produit.update_prix_total()  
            entrer_produit.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('liste_produits_sortants')  
    else:
        form = SortantClientForm()

    return render(request, 'enregistrement_produit_sortant.html', {'form': form})

@login_required
def modifier_produit_sortant(request, id):
    sortie_client_produit = get_object_or_404(Sortie_client, id=id)

    if request.method == 'POST':
        form = SortantClientForm(request.POST, instance=sortie_client_produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('liste_produits_sortants')
    else:
        form = SortantClientForm(instance=sortie_client_produit)

    return render(request, 'enregistrement_produit_sortant.html', {'form': form, 'sortie_client_produit': sortie_client_produit})

@login_required
def supprimer_produit_sortant(request, id):
    sortie_client_produit = get_object_or_404(Sortie_client, id=id)

    if request.method == 'POST':
        sortie_client_produit.delete()
        messages.success(request, "Operation reussit")
        next_param = request.GET.get('next', None)
        if next_param:
                return redirect(request.GET['next'])
        return redirect('liste_produits_sortants')

    return render(request, 'enregistrement_produit_sortant.html', {'sortie_client_produit': sortie_client_produit})

#les vues des produits sortants grossistes
@login_required
def liste_produits_sortants_grossiste(request):
    sortants_clients = Sortie_grossiste.objects.all()
    nombre_total_sortants_clients = sortants_clients.count()

    context = {
        'sortants_clients': sortants_clients,
        'nombre_total_sortants_clients': nombre_total_sortants_clients,
    }

    return render(request, 'liste_produits_sortants_grossiste.html', context)

@login_required
def enregistrement_produit_sortant_grossiste(request):
    form = SortantGrossisteForm()
    if request.method == 'POST':
        form = SortantGrossisteForm(request.POST)
        if form.is_valid():
            produit = request.POST['produit']
            quantite = int(request.POST['quantite'])
            if quantite > Stock.objects.filter(produit = produit).first().total_produit_restants:
                messages.warning(request, "La quantite que vous avez mis est superieur a celle du stock")
                return render(request, 'enregistrement_produit_sortant_grossiste.html', {'form': form})
            entrer_produit = form.save(commit=False)
            entrer_produit.update_prix_total()  
            entrer_produit.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('liste_produits_sortants_grossiste')  
    else:
        form = SortantGrossisteForm()

    return render(request, 'enregistrement_produit_sortant_grossiste.html', {'form': form})

@login_required
def modifier_produit_sortant_grossiste(request, id):
    sortie_grossiste_produit = get_object_or_404(Sortie_grossiste, id=id)

    if request.method == 'POST':
        form = SortantGrossisteForm(request.POST, instance=sortie_grossiste_produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('liste_produits_sortants')
    else:
        form = SortantGrossisteForm(instance=sortie_grossiste_produit)

    return render(request, 'enregistrement_produit_sortant.html', {'form': form, 'sortie_grossiste_produit': sortie_grossiste_produit})

@login_required
def supprimer_produit_sortant_grossiste(request, id):
    sortie_client_produit = get_object_or_404(Sortie_grossiste, id=id)

    if request.method == 'POST':
        sortie_client_produit.delete()
        messages.success(request, "Operation reussit")
        next_param = request.GET.get('next', None)
        if next_param:
            return redirect(request.GET['next'])
        return redirect('liste_produits_sortants_grossiste')

    return render(request, 'enregistrement_produit_sortant_grossiste.html', {'sortie_client_produit': sortie_client_produit})

#les vues des produits 
@login_required
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'liste_produits.html', {'produits': produits})

@login_required
def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('liste_produits')  
    else:
        form = ProduitForm()

    return render(request, 'ajouter_produit.html', {'form': form})

@login_required
def modifier_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)

    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Operation reussit")
            next_param = request.GET.get('next', None)
            if next_param:
                return redirect(request.GET['next'])
            return redirect('liste_produits')  
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'ajouter_produit.html', {'form': form, 'produit': produit})

@login_required
def supprimer_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)

    if request.method == 'POST':
        produit.delete()
        messages.success(request, "Operation reussit")
        next_param = request.GET.get('next', None)
        if next_param:
                return redirect(request.GET['next'])
        return redirect('liste_produits')  

    return render(request, 'ajouter_produit.html', {'produit': produit})
