"""
dansMonpanier
refresh data module
"""

from django.core.management.base import BaseCommand
import sys
sys.path.insert(1, '/home/dev/monpanier/explore/data')
from cat_builder import *
from food_builder import *
import psycopg2
import datetime

# Set up psycopg2
conn = psycopg2.connect(dbname=os.environ['DB_NAME'],
                        user=os.environ['DB_USER'],
                        host='localhost',
                        port='5432',
                        password=os.environ['DB_PW'],
                        )
cur = conn.cursor()


class Command(BaseCommand):
    args = ''
    help = 'Import fresh data to remote server'

    def handle(self, *args, **options):
        time = datetime.date.today()
        print("------------------------------")
        print("CRON REPORT  |  {}".format(time))
        print("Job run every Tuesday at 23:59")
        print("App: dansmonpanier")
        print("------------------------------\n")

        # A- Update category list
        print("1- Update category list:\n")
        cat = CatBuilder()
        cat.get_cat()
        print("- {} categories for {} items before wrangling.".format(cat.raw_cat, cat.raw_items))
        print("- {} categories for {} items after wrangling.".format(cat.clean_cat, cat.clean_items))
        cat_attrition = cat.raw_cat - cat.clean_cat
        item_attrition = cat.raw_items - cat.clean_items
        print("---> Data attrition = {} categories for {} items.".format(cat_attrition, item_attrition))
        # Filling db requires a tmp tab to import one specific field only
        # 1- Create temporary table
        cur.execute("CREATE TEMP TABLE category_tmp(category VARCHAR, items INT)")
        conn.commit()
        # 2- Copy csv
        copy_stmt = "COPY category_tmp (category, items) FROM '{}' DELIMITER ';' CSV HEADER".format(cat.pg_path)
        cur.execute(copy_stmt)
        conn.commit()
        # 3- Insert a specific field into the target table
        cur.execute("INSERT INTO explore_category(category) SELECT category FROM category_tmp")
        conn.commit()
        print("*** update completed.\n")
        # 4- Drop temp table
        cur.execute("DROP TABLE category_tmp")
        conn.commit()

        # B- Update food data
        print("2- Update food data:\n")
        for elt in cat_list_test:
            food = FoodBuilder(elt)
            # 1- Wrangle and save data from Open Food Facts db
            food.launch_request()
            print('- "{}" contains {} items before wrangling.'.format(food.cat, food.items))
            print('- "{}" contains {} items after wrangling.'.format(food.cat, food.clean_items))
            food_attrition = food.items - food.clean_items
            print("---> Data attrition = {} items.".format(food_attrition))
            # 2- Fill tab with fresh data
            fill_db = "COPY explore_food ({}) FROM '{}' DELIMITER ';' CSV HEADER".format(fields, food.csv_path)
            cur.execute(fill_db)
            conn.commit()
            print("*** update completed.\n")

        # C- Drop duplicates
        print("3- Drop duplicates:\n")
        cur.execute("SELECT COUNT(*) FROM explore_food")
        initial = cur.fetchone()
        print("- Initial total of items :", initial[0])
        cur.execute("DELETE FROM explore_food a USING explore_food b WHERE a.id < b.id and a.code = b.code")
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM explore_food")
        new = cur.fetchone()
        print("- New total of items :", new[0])
        row_attrition = initial[0] - new[0]
        print("---> Data attrition = {} rows.".format(row_attrition))
