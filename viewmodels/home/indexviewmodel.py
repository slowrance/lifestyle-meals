from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from starlette.requests import Request

# from services import package_service, user_service
from services import meals_service
from viewmodels.shared.viewmodel import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.target_carbs: Optional[int] = None
        self.target_proteins: Optional[int] = None
        self.target_fats: Optional[int] = None
        self.daily_meals = None
        self.random_meal = None
        self.valid_combo_count = None
        self.allergies = None
        self.dislikes = None

    async def load(self):
        form = await self.request.form()
        self.target_carbs = int(form.get('target_carbs'))
        self.target_proteins = int(form.get('target_proteins'))
        self.target_fats = int(form.get('target_fats'))
        self.allergies = form.getlist('allergies')
        self.dislikes = form.getlist('dislikes')

        if not self.target_carbs or self.target_carbs < 0:
            self.error = "Target Carbs must be a number greater than 0."
        if not self.target_proteins or self.target_proteins < 0:
            self.error = "Target Proteins must be a number greater than 0."
        if not self.target_fats or self.target_fats < 0:
            self.error = "Target Fats must be a number greater than 0."


