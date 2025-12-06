from app import app, db
from sqlalchemy import inspect

def inspect_db():
    with app.app_context():
        engine = db.engine
        print(f"Current Database URL: {engine.url}")

        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("\nDatabase included:")
        for t in tables:
            print(f"  - {t}")

        for t in tables:
            print(f"\n Field structure: {t}")
            for col in inspector.get_columns(t):
                name = col["name"]
                ctype = col["type"]
                nullable = col["nullable"]
                pk = col.get("primary_key", False)
                print(f"  - {name} ({ctype}), NULLABLE={nullable}, PK={pk}")

if __name__ == "__main__":
    inspect_db()

