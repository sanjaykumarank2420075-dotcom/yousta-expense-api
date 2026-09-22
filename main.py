from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from database import Base, engine, get_db
from models import Employee, Trip, Expense
from schemas import ExpenseCreate


app = FastAPI(
    title="Yousta Travel & Expense API",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Yousta Travel & Expense API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/trips/open")
def get_open_trips(
    employee_id: str,
    db: Session = Depends(get_db)
):

    trips = (
        db.query(Trip)
        .filter(
            Trip.employee_id == employee_id,
            Trip.status == "OPEN"
        )
        .all()
    )

    return {
        "employee_id": employee_id,
        "count": len(trips),
        "trips": [
            {
                "trip_id": trip.trip_id,
                "destination": trip.destination,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
                "purpose": trip.purpose,
                "status": trip.status
            }
            for trip in trips
        ]
    }


@app.post("/expenses")
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):

    # 1. Check employee
    employee = (
        db.query(Employee)
        .filter(
            Employee.employee_id == expense.employee_id
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    # 2. Check trip belongs to employee
    trip = (
        db.query(Trip)
        .filter(
            Trip.trip_id == expense.trip_id,
            Trip.employee_id == expense.employee_id
        )
        .first()
    )

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found for this employee"
        )


    # 3. Check trip is OPEN
    if trip.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail="Expense can only be added to an OPEN trip"
        )


    # 4. Create expense
    expense_id = (
        f"EXP-{uuid4().hex[:8].upper()}"
    )

    new_expense = Expense(
        expense_id=expense_id,
        employee_id=expense.employee_id,
        trip_id=expense.trip_id,
        category=expense.category,
        amount=expense.amount,
        currency=expense.currency,
        expense_date=expense.expense_date,
        description=expense.description,
        status="RECORDED"
    )


    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)


    return {
        "message": "Expense added successfully",

        "expense": {
            "expense_id": new_expense.expense_id,
            "employee_id": new_expense.employee_id,
            "trip_id": new_expense.trip_id,
            "category": new_expense.category,
            "amount": new_expense.amount,
            "currency": new_expense.currency,
            "expense_date": new_expense.expense_date,
            "description": new_expense.description,
            "status": new_expense.status
        }
    }

@app.post("/setup/seed")
def seed_database(db: Session = Depends(get_db)):

    existing_employee = (
        db.query(Employee)
        .filter(Employee.employee_id == "EMP001")
        .first()
    )

    if not existing_employee:
        employee = Employee(
            employee_id="EMP001",
            name="Sanjay Kumar",
            email="sanjay@yousta.com",
            grade="E2"
        )
        db.add(employee)

    existing_trip = (
        db.query(Trip)
        .filter(Trip.trip_id == "TRIP001")
        .first()
    )

    if not existing_trip:
        trip = Trip(
            trip_id="TRIP001",
            employee_id="EMP001",
            destination="Bangalore",
            start_date="2026-09-20",
            end_date="2026-09-23",
            purpose="Client Meeting",
            status="OPEN"
        )
        db.add(trip)

    db.commit()

    return {
        "message": "Seed data created successfully"
    }

@app.get("/expenses")
def get_expenses(
    employee_id: str,
    trip_id: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Expense).filter(
        Expense.employee_id == employee_id
    )

    if trip_id:
        query = query.filter(
            Expense.trip_id == trip_id
        )

    expenses = query.all()

    return {
        "employee_id": employee_id,
        "trip_id": trip_id,
        "count": len(expenses),
        "expenses": [
            {
                "expense_id": expense.expense_id,
                "trip_id": expense.trip_id,
                "category": expense.category,
                "amount": expense.amount,
                "currency": expense.currency,
                "expense_date": expense.expense_date,
                "description": expense.description,
                "status": expense.status
            }
            for expense in expenses
        ]
    }

@app.get("/expenses/total")
def get_total_expense(
    employee_id: str,
    trip_id: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Expense).filter(
        Expense.employee_id == employee_id
    )

    if trip_id:
        query = query.filter(
            Expense.trip_id == trip_id
        )

    expenses = query.all()

    total = sum(expense.amount for expense in expenses)

    return {
        "employee_id": employee_id,
        "trip_id": trip_id,
        "total_expense": total,
        "currency": expenses[0].currency if expenses else "INR",
        "expense_count": len(expenses)
    }