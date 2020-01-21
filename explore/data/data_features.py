#! /usr/bin/env python3
# coding: utf-8

"""
dansMonPanier data features
"""

import os

"""
Managing https requests
"""


# Get food categories
url = 'https://fr.openfoodfacts.org/categories'
target_col1 = 'Catégorie'
target_col2 = 'Produits'

# Set API Read Search address
address = "https://fr.openfoodfacts.org/cgi/search.pl?"

# Set advanced search criteria
cat_search = "tagtype_0=categories&tag_contains_0=contains&tag_0="
type = "&search_simple=1&action=process"
page_size = "&page_size="
pagination = "&page="
out_file = "&json=1"


"""
Managing data collection
"""

# Set keywords for indicators extraction
gluten_free = 'sans gluten|gluten-free|sin gluten|glutenfrei|sem gluten|senza glutine'
bio = 'bio|agriculture biologique|ökologischer landbau|agricultura orgânica|agricoltura biologica|' \
      'agricoltura biologica'
eco_packaging = 'point vert|info-tri-point-vert|green dot|punto verde|ponto verde|grüner punkt|' \
                'éco-emballages|öko-verpackung|eco-imballaggio|eco-embalagens|ecoembalaje'
made_in_france = 'fabriqué en france|made in france|made-in-france|hergestellt in frankreich|' \
                 'fabricado en francia|fabricado na frança|fatto in francia'
fair_trade = 'commerce équitable|fairtrade|fair trade|feira comercial|commercio equo|comercio justo|' \
             'fairer handel'

# Set column labels
vars = [
    'category_group',
    'created',
    'code',
    'name',
    'brands',
    'stores',
    'bio',
    'eco_packaging',
    'fsc',
    'utz',
    'palm_oil_free',
    'made_in_france',
    'ingredients_text',
    'additives',
    'allergens_from_ingredients',
    'quantity',
    'image_url',
    'packaging',
    'french_ingredients',
    'fair_trade',
    'vegan',
    'vegetarian',
    'gluten_free',
    'iplc',
    'nova',
    'nutrition_grade',
    'energy',
    'energy_unit',
    'fat',
    'saturated_fat',
    'sugars',
    'salt',
    'fiber',
    'proteins'
]

# Manage category import
off_cat = os.path.abspath('off_cat.csv')

# Manage food facts import
fields = """
    category_group,
    created,
    code,
    name,
    brands,
    stores,
    bio,
    eco_packaging,
    fsc,
    utz,
    palm_oil_free,
    made_in_france,
    ingredients_text,
    additives,
    allergens_from_ingredients,
    quantity,
    image_url,
    packaging,
    french_ingredients,
    fair_trade,
    vegan,
    vegetarian,
    gluten_free,
    iplc,
    nova,
    nutrition_grade,
    energy,
    energy_unit,
    fat,
    saturated_fat,
    sugars,
    salt,
    fiber,
    proteins
"""