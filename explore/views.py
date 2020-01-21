#! /usr/bin/env python3
# coding: utf-8

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
from .models import Category, Food, Favorite
from .forms import UserForm
from django.db.models import Q
from unidecode import unidecode


def index(request):
    """
    Function to return the home page.
    """
    return render(request, 'explore/index.html')


def results(request):
    """
    Function to return search results
    according to the user query.
    """
    q = request.GET.get('q')
    if q == '' or q == ' ' or len(q) < 3:
        # prevent empty query
        messages.warning(request, "Veuillez saisir un aliment.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        # Remove accents
        q = unidecode(q)
        q_ = q.split()
        # Put the main entity in the plural
        # if not the case
        if not q_[0].endswith('s') and not q_[0].endswith('x') and not q_[0].endswith('u') \
                and not q_[0].endswith('y'):
            plur = q_[0] + "s"
            q_[0] = plur
            q_ = " ".join(q_)
        else:
            q_ = q
        search = q.split()
        # Query the complete expression in category or name fields
        dataset = Food.objects.filter(Q(category_group__unaccent__icontains=q_) | Q(name__unaccent__icontains=q))
        if dataset.count() > 700:
            # Refine results
            dataset = Food.objects.filter(name__unaccent__startswith=search[0][:5].capitalize())
            if q == 'lait':
                dataset = dataset.exclude(name__icontains='laitue')
            if unidecode(q) == 'cafe':
                dataset = dataset.exclude(name__unaccent__icontains='cafeine')
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
            # filter results by fair_trade criteria
            data = results.filter(fsc=True)[:100]
        if data:
            if request.user.is_authenticated:
                # check the user favorite list
                # so to prevent duplicates
                registered = Favorite().ref_list(request)
                return render(request, 'explore/results.html', {'registered': registered, 'results': data})
            else:
                return render(request, 'explore/results.html', {'results': data})
        else:
            target = Category.objects.filter(category__icontains=q)
            if target:
                # save target for future db update
                with open('explore/data/cat_to_load.txt', 'a') as f:
                    f.write(str(target[0]) + ', ')
                messages.warning(request, 'La catégorie "{}" ne figure pas encore dans notre base.'.format(target[0]))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.warning(request, 'Aucun résultat ne correspond à votre recherche.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def item(request, id):
    """
    Function to return the features
    of a targeted product.
    """
    features = Food.objects.filter(id=id)
    if request.user.is_authenticated:
        registered = Favorite().ref_list(request)
        if registered:
            return render(request, 'explore/item.html',
                          {'features': features, 'registered': registered})
    else:
        return render(request, 'explore/item.html', {'features': features})


def save_favorites(request):
    """
    Function to register products
    as favorites.
    """
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            p = request.POST.get('p')
            new = Food.objects.get(pk=p)
            favorites = Favorite()
            favorites.products = new
            favorites.user = user
            favorites.save()
            messages.success(request, 'Produit enregistré !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.info(request, mark_safe(
            '<a href="/signin"><u>Connectez-vous ou inscrivez-vous</u></a> pour enregistrer des produits.'
        ))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def my_favorites(request):
    """
    Function to display
    the user's favorites.
    """
    if request.user.is_authenticated:
        user = request.user
        favorites = Food.objects.filter(favorite__user=user)
        if len(favorites) > 0:
            return render(request, 'explore/favorites.html', {'favorites': favorites})
        else:
            messages.info(request, mark_safe(
                'Vous n\'avez pas encore enregistré de produit. Lâchez-vous !'))
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))


def my_profile(request):
    """
    Function to return
    user profile.
    """
    if request.user.is_authenticated:
        return render(request, 'explore/profile.html', {})
    else:
        return HttpResponseRedirect(reverse('index'))


def signin(request):
    """
    Function to register
    new user.
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Bravo {}, vous avez rejoint la communauté !'.format(user.first_name))
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, 'Informations non conformes aux règles de sécurité.')
            return render(request, 'explore/signin.html', {'form': form})
    else:
        form = UserForm()
        return render(request, 'explore/signin.html', {'form': form})


def user_login(request):
    """
    Function to allow
    the user to log in.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Heureux de vous revoir, {} !'.format(user.first_name))
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, 'Identifiants incorrects.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return render(request, 'explore/signin.html', {})


def user_logout(request):
    """
    Function to allow
    the user to log out properly.
    """
    logout(request)
    messages.success(request, 'Merci de nous avoir rendu visite. A bientôt !')
    return HttpResponseRedirect(reverse('index'))


def legal(request):
    """
    Function to display
    the legal notice.
    """
    return render(request, 'explore/legal.html', {})
