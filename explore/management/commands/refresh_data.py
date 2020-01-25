"""
TheRightFood module
to refresh data
"""

from django.core.management.base import BaseCommand
from explore.data.data_features import *
from explore.data.food_builder import *
import psycopg2
import glob
import os


class Command(BaseCommand):
    args = ''
    help = 'Export data to remote server'

    def handle(self, *args, **options):

        # Load and wrangle data from Open Food Facts db
        for elt in cat_list:
            FoodBuilder(elt).launch_request()
            print("{} loaded ".format(elt))

        # Set up psycopg2
        conn = psycopg2.connect(dbname=os.environ['DB_NAME'],
                                user=os.environ['DB_USER'],
                                host='',
                                port='5432',
                                password=os.environ['DB_PW'],
                                )
        cur = conn.cursor()

        # A- Fill Category tab
        # requires a tmp tab to import one specific field only

        # 1- Create temporary table
        cur.execute("CREATE TEMP TABLE category_tmp(category VARCHAR, items INT)")
        conn.commit()

        # 2- Copy csv
        copy_stmt = "COPY category_tmp (category, items) FROM '{}' DELIMITER ';' CSV HEADER".format(off_cat_pg)
        cur.execute(copy_stmt)
        conn.commit()

        # 3- Insert a specific field into the target table
        cur.execute("INSERT INTO explore_category(category) SELECT category FROM category_tmp")
        conn.commit()

        # 4- Drop temp table
        cur.execute("DROP TABLE category_tmp")
        conn.commit()

        # B- Fill Food tab
        extension = '_dataset.csv'
        csv = [i for i in glob.glob('*{}'.format(extension))]
        files = []
        for item in csv:
            file = os.path.abspath(item)
            files.append(file)
            for f in files:
                fill_db_ = "COPY explore_food ({}) FROM '{}' DELIMITER ';' CSV HEADER".format(fields, f)
                cur.execute(fill_db_)
                conn.commit()

        # C- Drop duplicates
        cur.execute("DELETE FROM explore_food a USING explore_food b WHERE a.id < b.id and a.code = b.code")
        conn.commit()
