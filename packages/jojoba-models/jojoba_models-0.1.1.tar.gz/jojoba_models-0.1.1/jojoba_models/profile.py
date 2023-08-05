from typing import List

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Employee(Base):

    __tablename__ = "employees"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]


class Employer(Base):

    __tablename__ = "employers"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]

    positions: Mapped[List["Position"]] = relationship(back_populates="employer")


class Position(Base):

    __tablename__ = "positions"

    position_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("employers.user_id"))
    title: Mapped[str]
    description: Mapped[str]

    employer: Mapped[Employer] = relationship(back_populates="positions")
