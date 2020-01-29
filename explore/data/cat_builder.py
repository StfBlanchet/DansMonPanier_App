"""
dansMonPanier category builder
"""

import requests
import pandas as pd
import sys
sys.path.insert(1, '/home/dev/monpanier/explore/data')
from data_features import *


class CatBuilder:

    def __init__(self):
        self.url = url
        self.target_col1 = target_col1
        self.target_col2 = target_col2
        self.raw_cat = int()
        self.raw_items = int()
        self.clean_cat = int()
        self.clean_items = int()
        self.pd_path = str()
        self.pg_path = str()

    def get_cat(self):
        """
        Method to get currently available OFF categories
        and clean them
        """
        r = requests.get(self.url)
        data = pd.read_html(r.content)[0][[self.target_col1, self.target_col2]]
        self.df = pd.DataFrame(data)
        self.df.columns = ['category', 'items']
        self.raw_cat = len(self.df.index)
        self.raw_items = self.df['items'].sum()

        # Check NaN
        self.df.dropna(subset=['category'], how='any', inplace=True)

        # Check duplicated categories
        self.df['category'] = self.df['category'].str.replace('-', ' ').str.replace(r'en:|fr:|es:|it:|de:', '')
        self.df['category'] = self.df['category'].str.lower()
        self.df.drop_duplicates(subset=['category'], keep='first', inplace=True)

        # Discard poor cat
        poor_cat = self.df.loc[self.df['items'] < 100]
        self.df.drop(poor_cat.index, inplace=True)

        # Check data attrition
        self.clean_cat = len(self.df.index)
        self.clean_items = self.df['items'].sum()

        # Save clean df
        self.df.reset_index(drop=True)
        # for pandas use (with "," separator)
        self.pd_path = os.path.join(my_path, "../data/off_cat.csv")
        self.df.to_csv(self.pd_path, sep=',', index=False)
        # for postgres use (with ";" separator)
        self.pg_path = os.path.join(my_path, "../data/off_cat_pg.csv")
        self.df.to_csv(self.pg_path, sep=';', index=False)
