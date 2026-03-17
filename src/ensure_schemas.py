# src/ensure_columns.py
from sqlalchemy import inspect, text
from src.database import engine

# Define what you expect in the DB: table -> list of columns
REQUIRED_COLUMNS = {
    "employees": ["hashed_password"],
    # "projects": ["some_column"],
    # "tasks": ["another_column"],
}


def ensure_columns(required_columns: dict[str, list[str]]):
    insp = inspect(engine)
    created_any = False

    for table_name, columns in required_columns.items():
        # Check table existence
        if not insp.has_table(table_name, schema="public"):
            print(f"nothing changed for {table_name} (table does not exist)")
            continue

        # Existing columns in DB for this table
        existing_cols = {c["name"] for c in insp.get_columns(table_name, schema="public")}

        # Columns missing in DB
        missing = [col for col in columns if col not in existing_cols]
        if not missing:
            print(f"nothing changed for {table_name} (all columns already exist)")
            continue

        # Add each missing column (text NULL by default; customize per column if needed)
        with engine.begin() as conn:
            for col in missing:
                conn.execute(
                    text(
                        f'ALTER TABLE public."{table_name}" '
                        f'ADD COLUMN "{col}" text'
                    )
                )
                print(f'completed: added column "{col}" to table "{table_name}"')
                created_any = True

    if not created_any:
        print("nothing changed overall (no columns created)")


if __name__ == "__main__":
    ensure_columns(REQUIRED_COLUMNS)
