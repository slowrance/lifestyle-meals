import itertools
import random

import fastapi
from fastapi_chameleon import template
from starlette.requests import Request

from services.meals_service import get_meals, get_combos, get_valid_combos, apply_filters
from viewmodels.home.indexviewmodel import IndexViewModel
from viewmodels.shared.viewmodel import ViewModelBase

router = fastapi.APIRouter()


@router.get('/')
@template()
def index(request: Request):
    vm = IndexViewModel(request)
    return vm.to_dict()

@router.post('/')
@template()
async def index(request: Request):
    vm = IndexViewModel(request)
    await vm.load()
    combos = get_combos(vm.meal_size, vm.meal_count, vm.include_breakfast)
    valid_combos = get_valid_combos(combos, vm.target_carbs, vm.target_proteins, vm.target_fats)
    filtered_combos = apply_filters(valid_combos, vm.allergies, vm.dislikes)
    random_meal = random.choice(filtered_combos)
    if len(filtered_combos) < 6:
        vm.daily_meals = filtered_combos
    else:
        vm.daily_meals = random.sample(filtered_combos, 6)
    vm.random_meal = random_meal
    vm.valid_combo_count = len(filtered_combos)
    return vm.to_dict()
