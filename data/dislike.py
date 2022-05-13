import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase


class Dislike(SqlAlchemyBase):
    __tablename__ = 'dislikes'

    id: str = sa.Column(sa.Integer, primary_key=True)
    name: str = sa.Column(sa.String, nullable=False)
