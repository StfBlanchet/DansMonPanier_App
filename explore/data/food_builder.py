"""
dansMonPanier Data Builder
"""


import pandas as pd
from unidecode import unidecode
import re
from math import *
import requests
import datetime
import sys
sys.path.insert(1, '/home/dev/monpanier/explore/data')
from data_features import *


"""
This class allows to automate 
data cleaning and collection.
"""


class FoodBuilder:

    def __init__(self, target):
        self.df = pd.read_csv(off_cat)
        self.cat = str(target)
        # get the number of items in the target category
        self.row = self.df[self.df.category == self.cat].reset_index(drop=True)
        self.items = self.row.iat[0, 1]
        self.pages = []
        self.clean_items = int()
        self.csv_path = str()

    def launch_request(self):
        """
        Method to automate URIs generation for a target category
        """
        self.pages = []
        self.uris = []
        items_per_page = 1000
        # Format a list to generate queries properly
        self.uris_cat = unidecode(self.cat)
        self.uris_cat = self.uris_cat.replace(' ', '-')
        # Define pagination according to the nb of products per cat.
        if self.items > items_per_page:
            # get 1000 items per page
            x = ceil(self.items/items_per_page)
        else:
            x = 1
        # store nb of pages per cat
        self.pages.append(x)
        # get pagination starting at 1
        for i in range(1, self.pages[0]+1):
            uri = address + cat_search + self.uris_cat + type +\
                  page_size + str(items_per_page) + pagination + str(i) + out_file
            self.uris.append(uri)
        self.data_miner()

    def data_miner(self):
        """
        Method to send requests and filter the collected data
        """
        self.cat_data = dict()
        for uri in self.uris:
            r = requests.get(uri)
            data = r.json()
            for j in range(len(data['products'])):
                main = data['products'][j]
                nutriments = main['nutriments']
                n = ''
                pagin = str(data['page']) + '_' + str(j)
                # select relevant product facts
                self.cat_data.update({pagin: {
                    'category': self.cat,
                    'category_group': main.get('categories', n),
                    'created': str(datetime.date.today()),
                    'code': main.get('code', n),
                    'name': main.get('product_name', n),
                    'brands': main.get('brands', n),
                    'stores': main.get('stores', n),
                    'completeness': main.get('completeness', n),
                    'origins': main.get('origins', n),
                    'ingredients_text': main.get('ingredients_text', n),
                    'additives': main.get('additives_n', n),
                    'allergens_from_ingredients': main.get('allergens_from_ingredients', n),
                    'quantity': main.get('quantity', n),
                    'image_url': main.get('image_url', n),
                    'packaging': main.get('packaging', n),
                    'labels': main.get('labels', n),
                    'ingredients': main.get('ingredients_analysis_tags', n),
                    'nova': main.get('nova_group', n),
                    'nutrition_grade': main.get('nutrition_grades', n),
                    'energy': nutriments.get('energy', n),
                    'energy_unit': nutriments.get('energy_unit', n),
                    'fat': nutriments.get('fat', n),
                    'saturated_fat': nutriments.get('saturated-fat', n),
                    'sugars': nutriments.get('sugars', n),
                    'salt': nutriments.get('salt', n),
                    'proteins': nutriments.get('proteins', n),
                    'fiber': nutriments.get('fiber', n)}
                })
        self.res = pd.DataFrame(self.cat_data).T
        self.data_wrangler()

    def data_wrangler(self):
        """
        Method to clean, refine and enrich the data set
        """

        # Drop rows where product profile completeness is missing or < 90%
        self.res.drop(self.res[self.res.completeness == ''].index, inplace=True)
        self.res.drop(self.res[self.res.completeness.astype(float) < 0.9].index, inplace=True)

        # Remove undesired tags from cols containing text
        cleaner_0 = re.compile(r'[\t\n\r"_*]')
        cleaner_1 = r'fr:|en:|es:|it:|de:'
        text_cols = ['name',
                     'brands',
                     'stores',
                     'ingredients_text',
                     'allergens_from_ingredients',
                     'quantity',
                     'packaging']
        for var in text_cols:
            self.res[var] = self.res[var].str.replace(cleaner_0, '').str.replace(';', ',').str.replace(cleaner_1, '')

        # Remove duplicates
        text_cols_dup = ['name',
                         'brands',
                         'stores',
                         'allergens_from_ingredients',
                         'packaging']
        content = dict()
        for var in text_cols_dup:
            self.res[var] = self.res[var].str.lower()
            item = self.res[var].str.replace(' ,', ',').str.replace('  ,', ',').str.replace(', ', ',').str.replace(',  ', ',').str.replace(' , ', ',')
            content.update({var: item})
            for i in range(len(self.res)):
                c = str(content[var][i]).split(',')
                c = list(dict.fromkeys(c))
                if len(c) > 15:
                    c = c[:15]
                content[var][i] = ', '.join(c)
        text_cleaned = pd.DataFrame(content)
        cap_col = ['name', 'brands', 'stores']
        for var in cap_col:
            text_cleaned[var] = text_cleaned[var].str.title()

        # Extract relevant indicators (or allegations)
        self.res.labels = self.res.labels.str.lower()
        self.res['bio'] = self.res.labels.str.contains(bio)
        self.res['eco_packaging'] = self.res.labels.str.contains(eco_packaging)
        self.res['fsc'] = self.res.labels.str.contains('fsc')
        self.res['utz'] = self.res.labels.str.contains('utz')
        self.res['made_in_france'] = self.res.labels.str.contains(made_in_france)
        self.res['fair_trade'] = self.res.labels.str.contains(fair_trade)
        self.res['gluten_free'] = self.res.labels.str.contains(gluten_free)
        self.res['iplc'] = self.res.labels.str.contains('iplc')
        self.res.origins = self.res.origins.str.lower()
        self.res['french_ingredients'] = self.res.origins.str.contains('france')
        text_enriched = pd.DataFrame(self.res.ingredients.values.tolist(),
                             columns=['palm_oil_free', 'vegan', 'vegetarian'], index=self.res.index)
        text_enriched.palm_oil_free = text_enriched.palm_oil_free.str.contains('en:palm-oil-free')
        text_enriched.vegan = text_enriched.vegan.str.contains('en:vegan')
        text_enriched.vegetarian = text_enriched.vegetarian.str.contains('en:vegetarian')

        # Merge dataframes
        self.res = self.res.join(text_enriched)
        self.res = self.res.drop(text_cols_dup, axis=1)
        self.res = self.res.join(text_cleaned)

        # Check data attrition
        self.clean_items = len(self.res.index)

        # Save
        csv_name = self.uris_cat.replace("'", "-") + '_dataset.csv'
        self.csv_path = os.path.join(my_path, "../data/", csv_name)
        self.res.to_csv(self.csv_path, index=False, sep=';', header=True, columns=vars)
