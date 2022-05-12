import os
import sys
import csv


sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..")))

import data.db_session as db_session
from data.meal import Meal


def main():
    init_db()
    session = db_session.create_session()
    meal_count = session.query(Meal).count()
    session.close()
    if meal_count == 0:
        file_data = do_load_file()
        do_meal_import(file_data)
    do_summary()

def do_load_file():
    filename = 'meals2.csv'
    with open(filename, mode='r') as f:
        meals = list(csv.DictReader(f))
    return meals

def do_meal_import(meals: list):
    session = db_session.create_session()
    for line in meals:
        meal = Meal()
        meal.size = line['size']
        meal.name = line['name']
        meal.type = line['type']
        meal.carbs = line['carbs']
        meal.proteins = line['proteins']
        meal.fats = line['fats']

        session.add(meal)
    session.commit()


def do_summary():
    session = db_session.create_session()

    print("Final numbers:")
    print("Meals: {:,}".format(session.query(Meal).count()))


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'meals.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)

if __name__ == '__main__':
    main()
