"""
dansMonPanier app
File that manages views.
"""


from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Food, Favorite
from .forms import UserForm
from .process import *
from django.db.models import Q


def index(request):
    """
    Function to return the home page.
    """
    header = 'masthead'
    title = 'Je sais ce que je mange !'
    return render(request, 'explore/index.html', {'class': header, 'title': title})


def results(request):
    """
    Function to return search results
    according to the user query.
    """
    header = 'master'
    title = 'Faites le bon choix !'
    raw_query = request.GET.get('q')
    rq = raw_query.split()
    if len(rq) == 0 or len(rq[0]) < 3:
        # prevent empty query
        messages.info(request, 'Veuillez saisir un aliment.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        # Remove accents and pluralize
        q = Process().pluralize(raw_query)
        # Query the complete expression in category_group field
        dataset = Food.objects.filter(category_group__unaccent__icontains=q)
        if not dataset:
            # Query the first two words only in category_group field
            dataset = Food.objects.filter(category_group__unaccent__startswith=q[:1])
        # Rank results
        ranking = request.GET.get('ranking')
        results = dataset
        if ranking == 'nutrition':
            # order results by nutrition grade
            results = dataset.order_by('nutrition_grade')
        elif ranking == 'nova':
            # order results by nova group
            results = dataset.order_by('nova')
        # Filter results
        filtering = request.GET.get('filtering')
        data = results
        if filtering == 'none':
            data = results[:100]
        if filtering == 'made-in-france':
            # filter results by made_in_france criteria
            data = results.filter(Q(made_in_france=True) | Q(french_ingredients=True))[:100]
        elif filtering == 'bio':
            # filter results by "bio" criteria
            data = results.filter(bio=True)[:100]
        elif filtering == 'palm-oil-free':
            # filter results by palm_oil_free criteria
            data = results.filter(Q(palm_oil_free=True) | Q(name__icontains='sans huile de palme'))[:100]
        elif filtering == 'fair-trade':
            # filter results by fair_trade criteria
            data = results.filter(fair_trade=True)[:100]
        elif filtering == 'fsc':
            # filter results by fsc criteria
            data = results.filter(fsc=True)[:100]
        if data:
            context = {'results': data, 'class': header, 'title': title}
            if request.user.is_authenticated:
                # check the user favorite list
                # so to prevent duplicates
                registered = Favorite().ref_list(request)
                context = {'registered': registered, 'results': data, 'class': header, 'title': title}
            return render(request, 'explore/results.html', context)
        else:
            messages.info(request, 'Aucun résultat ne correspond à votre recherche.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def item(request, id):
    """
    Function to return the features
    of a targeted product.
    """
    header = 'food_item'
    features = Food.objects.filter(id=id)
    context = {'features': features, 'class': header}
    if request.user.is_authenticated:
        registered = Favorite().ref_list(request)
        context = {'features': features, 'class': header, 'registered': registered}
    return render(request, 'explore/item.html', context)


def save_favorites(request):
    """
    Function to register products
    as favorites.
    """
    if request.user.is_authenticated:
        p = request.POST.get('p')
        product = Food.objects.get(pk=p)
        Favorite(products=product, user=request.user).save()
        msg = 'Produit enregistré !'
    else:
        msg = mark_safe('<a href="/signin"><u>Connectez-vous ou inscrivez-vous</u></a> pour enregistrer des produits.')
    messages.info(request, msg)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def my_favorites(request):
    """
    Function to display
    the user's favorites.
    """
    header = ['master', 'masthead']
    title = ['Mes favoris', 'Pas encore de favoris ?']
    if request.user.is_authenticated:
        favorites = Food.objects.filter(favorite__user=request.user)
        if len(favorites) > 0:
            context = {'favorites': favorites, 'class': header[0], 'title': title[0]}
            temp = 'explore/favorites.html'
        else:
            context = {'class': header[1], 'title': title[1]}
            temp = 'explore/index.html'
        return render(request, temp, context)
    else:
        return HttpResponseRedirect(reverse('index'))


def remove_favorites(request):
    """
    Function to remove products
    from favorites.
    """
    if request.user.is_authenticated:
        r = request.POST.get('r')
        Favorite.objects.filter(Q(products=r) & Q(user=request.user)).delete()
        messages.info(request, 'Produit supprimé !')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def my_profile(request):
    """
    Function to return
    user profile.
    """
    if request.user.is_authenticated:
        header = 'master'
        user = request.user
        title = user.first_name
        return render(request, 'explore/profile.html', {'class': header, 'title': title})
    else:
        return HttpResponseRedirect(reverse('index'))


def signin(request):
    """
    Function to register
    new user.
    """
    header = 'master'
    title = 'Votre espace'
    form = UserForm(request.POST)
    context = {'form': form, 'class': header, 'title': title}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = 'Bravo {}, vous avez rejoint la communauté !'.format(user.first_name)
            messages.info(request, msg)
            return HttpResponseRedirect(reverse('index'))
        else:
            msg = 'Informations erronées ou non conformes aux règles de sécurité. Veuillez recommencer.'
            messages.info(request, msg)
    return render(request, 'explore/signin.html', context)
  

def user_login(request):
    """
    Function to allow
    the user to log in.
    """
    header = 'master'
    title = 'Votre espace'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            msg = 'Heureux de vous revoir, {} !'.format(user.first_name)
            messages.info(request, msg)
            return HttpResponseRedirect(reverse('index'))
        else:
            msg = 'Identifiants incorrects.'
            messages.info(request, msg)
    return render(request, 'explore/signin.html', {'class': header, 'title': title})


def user_logout(request):
    """
    Function to allow
    the user to log out properly.
    """
    logout(request)
    messages.info(request, 'Merci de nous avoir rendu visite. A bientôt !')
    return HttpResponseRedirect(reverse('index'))


def legal(request):
    """
    Function to display
    the legal notice.
    """
    header = 'master'
    title = 'Mentions légales'
    return render(request, 'explore/legal.html', {'class': header, 'title': title})
