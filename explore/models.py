"""
dansMonPanier app
File that manages the creation
of the database.
"""

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    This class is used to create the table
    containing the different categories
    available in Open Food Facts database,
    and the number of items per category.
    """
    category = models.CharField(max_length=250)

    def __str__(self):
        return str(self.category)


class Food(models.Model):
    """
    This class is used to create the table
    containing the different variables
    associated with the products.
    """
    category_group = models.CharField(max_length=800)
    created = models.DateField()
    code = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=350, null=True)
    brands = models.CharField(max_length=250, null=True)
    stores = models.CharField(max_length=800, null=True)
    bio = models.CharField(max_length=5, null=True)
    eco_packaging = models.CharField(max_length=5, null=True)
    fsc = models.CharField(max_length=5, null=True)
    utz = models.CharField(max_length=5, null=True)
    palm_oil_free = models.CharField(max_length=5, null=True)
    made_in_france = models.CharField(max_length=5, null=True)
    ingredients_text = models.TextField(max_length=800, null=True)
    additives = models.IntegerField(null=True)
    allergens_from_ingredients = models.CharField(max_length=800, null=True)
    quantity = models.CharField(max_length=250, null=True)
    image_url = models.URLField(max_length=450, null=True)
    packaging = models.CharField(max_length=250, null=True)
    french_ingredients = models.CharField(max_length=5, null=True)
    fair_trade = models.CharField(max_length=5, null=True)
    vegan = models.CharField(max_length=5, null=True)
    vegetarian = models.CharField(max_length=5, null=True)
    gluten_free = models.CharField(max_length=5, null=True)
    iplc = models.CharField(max_length=5, null=True)
    nova = models.IntegerField(null=True)
    nutrition_grade = models.CharField(max_length=1, null=True)
    energy = models.FloatField(null=True)
    energy_unit = models.CharField(max_length=5, null=True)
    fat = models.FloatField(null=True)
    saturated_fat = models.FloatField(null=True)
    sugars = models.FloatField(null=True)
    salt = models.FloatField(null=True)
    fiber = models.FloatField(null=True)
    proteins = models.FloatField(null=True)

    def __str__(self):
        return self.category_group


class Favorite(models.Model):
    """
    This class is used to create the table
    that stores the products selected as
    favorites by the users.
    """
    products = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.CharField(max_length=15, null=True)

    def ref_list(self, request):
        """
        Method to return the list
        of products already saved
        by the user and avoid them
        to be selected twice.
        """
        user = request.user
        if user:
            items = Favorite.objects.filter(user=user).values_list('products')
            registered = []
            for item in items:
                registered.append(item[0])

            return registered
