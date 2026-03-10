from src.database import SessionLocal
from src.models import Employee 

def seed_employees():
    db = SessionLocal()
    try: 
        # only if table is empty
        if db.query(Employee).count() > 0:
            print("Employees already seeded, skipping.")
            return
        
        employees = [
            Employee(full_name="Alice Developer",  email="alice@example.com", role="developer"),
            Employee(full_name="Bob Manager",      email="bob@example.com",   role="manager"),
            Employee(full_name="Carol Tester",     email="carol@example.com", role="tester"),
        ]

        db.add_all(employees)
        db.commit()
        print("Seeded employees successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_employees()