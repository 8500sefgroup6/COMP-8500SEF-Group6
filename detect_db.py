from app import app, db
from sqlalchemy import inspect

def inspect_db():
    with app.app_context():
        engine = db.engine
        print(f"✅ 当前数据库 URL: {engine.url}")

        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("\n📋 数据库包含的表:")
        for t in tables:
            print(f"  - {t}")

        for t in tables:
            print(f"\n🔎 表结构: {t}")
            for col in inspector.get_columns(t):
                name = col["name"]
                ctype = col["type"]
                nullable = col["nullable"]
                pk = col.get("primary_key", False)
                print(f"  - {name} ({ctype}), NULLABLE={nullable}, PK={pk}")

if __name__ == "__main__":
    inspect_db()

