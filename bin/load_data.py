import os
import sys
import json
from typing import List

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..")))

import data.db_session as db_session
from data.meal import Meal
from data.allergy import Allergy
from data.dislike import Dislike


def main():
    init_db()
    session = db_session.create_session()
    meal_count = session.query(Meal).count()
    session.close()
    if meal_count == 0:
        data = do_load_json_file()
        do_meal_import(data)
    do_summary()

def do_load_json_file():
    filename = 'meals.json'
    try:
        with open(filename, 'r', encoding='utf-8') as fin:
            data = json.load(fin)
    except Exception as x:
        print("ERROR in file: {}, details: {}".format(filename, x), flush=True)
        raise

    return data

def do_meal_import(data):
    for meal in data['meals']:
        m = Meal()
        m.id = meal['id']
        m.name = meal['name']
        m.size = meal['size']
        m.type = meal['type']
        m.carbs = meal['carbs']
        m.proteins = meal['proteins']
        m.fats = meal['fats']
        allergies = build_allergies(m.id, meal['allergies'])
        dislikes = build_dislikes(m.id, meal['dislikes'])

        session = db_session.create_session()
        session.add(m)
        session.add_all(allergies)
        session.add_all(dislikes)
        session.commit()
        session.close()

def build_allergies(meal_id: int, allergies: List[str]) -> List[Allergy]:
    db_allergies = []
    for allergy in allergies:
        a = Allergy()
        a.name = allergy
        a.meal_id = meal_id
        db_allergies.append(a)
    return db_allergies

def build_dislikes(meal_id: int, dislikes: List[str]) -> List[Dislike]:
    db_dislikes = []
    for dislike in dislikes:
        d = Dislike()
        d.name = dislike
        d.meal_id = meal_id
        db_dislikes.append(d)
    return db_dislikes


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
