import itertools
import random

import fastapi
from fastapi_chameleon import template
from starlette.requests import Request

from services.meals_service import get_meals, get_combos, get_valid_combos
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
    combos = get_combos('Large')
    valid_combos = get_valid_combos(combos, vm.target_carbs, vm.target_proteins, vm.target_fats)
    random_meal = random.choice(valid_combos)
    vm.daily_meals = valid_combos
    vm.random_meal = random_meal
    vm.valid_combo_count = len(valid_combos)
    return vm.to_dict()
