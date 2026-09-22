from database import SessionLocal
from models import Employee, Trip


db = SessionLocal()


employee = Employee(
    employee_id="EMP001",
    name="Sanjay Kumaran K",
    email="sanjay.kumarank@hcl.com",
    grade="E2"
)


trip = Trip(
    trip_id="TRIP001",
    employee_id="EMP001",
    destination="Bangalore",
    start_date="2026-09-20",
    end_date="2026-09-23",
    purpose="Client Meeting",
    status="OPEN"
)


db.add(employee)
db.add(trip)

db.commit()
db.close()


print("Test data inserted successfully")