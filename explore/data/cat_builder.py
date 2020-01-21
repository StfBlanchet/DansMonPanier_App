#! /usr/bin/env python3
# coding: utf-8

"""
dansMonPanier category builder
"""

import requests
import pandas as pd
from data_features import *


class CatBuilder:

    def __init__(self):
        self.url = url
        self.target_col1 = target_col1
        self.target_col2 = target_col2

    def get_cat(self):
        """
        Method to get currently available OFF categories
        and clean them
        """
        r = requests.get(self.url)
        data = pd.read_html(r.content)[0][[self.target_col1, self.target_col2]]
        self.df = pd.DataFrame(data)
        self.df.columns = ['category', 'items']

        # Check NaN
        self.df.dropna(subset=['category'], how='any', inplace=True)

        # Check duplicated categories
        self.df['category'] = self.df['category'].str.replace('-', ' ').str.replace(r'en:|fr:|es:|it:|de:', '')
        self.df['category'] = self.df['category'].str.lower()
        self.df.drop_duplicates(subset=['category'], keep='first', inplace=True)

        # Discard poor cat
        poor_cat = self.df.loc[self.df['items'] < 100]
        self.df.drop(poor_cat.index, inplace=True)

        # Save clean df
        self.df.reset_index(drop=True)
        self.df.to_csv('off_cat.csv', sep=';', index=False)


CatBuilder().get_cat()
