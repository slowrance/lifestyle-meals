import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase


class Meal(SqlAlchemyBase):
    __tablename__ = 'meals'

    id: str = sa.Column(sa.Integer, primary_key=True)
    size: str = sa.Column(sa.String, nullable=False)
    name: str = sa.Column(sa.String, nullable=False)
    type: str = sa.Column(sa.String, nullable=False)
    carbs: int = sa.Column(sa.Integer, nullable=False)
    proteins: int = sa.Column(sa.Integer, nullable=False)
    fats: int = sa.Column(sa.Integer, nullable=False)


    def __repr__(self):
        return '<Meal {}>'.format(self.id)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if isinstance(other, Meal):
            return self.__repr__() == other.__repr__()
        else:
            return False
