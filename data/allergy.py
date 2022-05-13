
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase


class Allergy(SqlAlchemyBase):
    __tablename__ = 'allergies'

    id: str = sa.Column(sa.Integer, primary_key=True)
    name: str = sa.Column(sa.String, nullable=False)

    meal_id: int = sa.Column(sa.Integer, sa.ForeignKey('meals.id'))
    meal = orm.relationship('Meal')

    def __repr__(self):
        return f'<Alergy({self.name})>'

