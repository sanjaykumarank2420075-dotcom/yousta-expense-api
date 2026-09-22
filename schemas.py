from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    employee_id: str
    trip_id: str
    category: str
    amount: float
    currency: str
    expense_date: str
    description: str