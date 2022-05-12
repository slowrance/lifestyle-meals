import itertools
from typing import List

from sqlalchemy import select

from data import db_session
from data.meal import Meal


def get_meals(meal_type: str, meal_size: str) -> List[Meal]:
    session = db_session.create_session()
    query = select(Meal).where(Meal.type == meal_type, Meal.size == meal_size)
    results = session.execute(query)
    meals = [r[0] for r in results]
    for meal in meals:
        meal.calories = meal.carbs * 4 + meal.proteins * 4 + meal.fats * 9
    return meals

def get_combos(meal_size):
    breakfasts = get_meals('Breakfast', meal_size)
    entrees = get_meals('Entree', meal_size)
    entrees = list(itertools.combinations_with_replacement(entrees, 2))
    combos = list(itertools.product(breakfasts, entrees))
    combos = [flatten2list(combo) for combo in combos]
    daily_meals = []
    for combo in combos:
        daily_meals.append({'breakfast': combo[0], 'lunch': combo[1], 'dinner': combo[2]})
    print(len(combos))
    return daily_meals

def get_valid_combos(combos, target_carbs, target_proteins, target_fats):
    wiggle_room = 5
    valid_combos = []
    for combo in combos:
        carbs = combo['breakfast'].carbs + combo['lunch'].carbs + combo['dinner'].carbs
        proteins = combo['breakfast'].proteins + combo['lunch'].proteins + combo['dinner'].proteins
        fats = combo['breakfast'].fats + combo['lunch'].fats + combo['dinner'].fats
        if carbs <= target_carbs + wiggle_room and proteins <= target_proteins + wiggle_room and fats <= target_fats + wiggle_room:
            valid_combos.append(combo)
    print(len(valid_combos))
    return valid_combos

def flatten2list(object):
    gather = []
    for item in object:
        if isinstance(item, (list, tuple, set)):
            gather.extend(flatten2list(item))
        else:
            gather.append(item)
    return gather