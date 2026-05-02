import bcrypt
from src.database import SessionLocal
from models import Employee


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed_employees():
    db = SessionLocal()
    try:
        # wipe existing employees
        deleted_count = db.query(Employee).delete()
        db.commit()
        print(f"Deleted {deleted_count} existing employees.")

        employees = [
            Employee(
                full_name="Alice Developer",
                email="alice@example.com",
                role="developer",
                hashed_password=hash_password("temppassword123"),
            ),
            Employee(
                full_name="Bob Manager",
                email="bob@example.com",
                role="manager",
                hashed_password=hash_password("temppassword123"),
            ),
            Employee(
                full_name="Carol Tester",
                email="carol@example.com",
                role="tester",
                hashed_password=hash_password("temppassword123"),
            ),
            Employee(
                full_name="Gabe Gonzalez",
                email="gabe@example.com",
                role="administrator",
                hashed_password=hash_password("password1234"),
            ),
        ]

        db.add_all(employees)
        db.commit()
        print("Seeded employees successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_employees()
