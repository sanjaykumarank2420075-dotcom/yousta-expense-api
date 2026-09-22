from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    grade = Column(String, nullable=False)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(String, unique=True, nullable=False)
    employee_id = Column(String, nullable=False)

    destination = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    purpose = Column(String, nullable=False)

    status = Column(String, nullable=False)


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    expense_id = Column(
        String,
        unique=True,
        nullable=False
    )

    employee_id = Column(
        String,
        nullable=False
    )

    trip_id = Column(
        String,
        nullable=False
    )

    category = Column(
        String,
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    currency = Column(
        String,
        nullable=False
    )

    expense_date = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )