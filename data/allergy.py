import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase


class Allergy(SqlAlchemyBase):
    __tablename__ = 'allergies'

    id: str = sa.Column(sa.Integer, primary_key=True)
    name: str = sa.Column(sa.String, nullable=False)

