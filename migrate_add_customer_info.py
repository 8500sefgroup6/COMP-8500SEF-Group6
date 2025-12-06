from app import app, db
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE `order` ADD COLUMN customer_name VARCHAR(80)"))
            print("customer_name has been added")
        except Exception as e:
            print("customer_name may already exist:", e)

        try:
            conn.execute(text("ALTER TABLE `order` ADD COLUMN customer_phone VARCHAR(20)"))
            print("customer_phone may already exist")
        except Exception as e:
            print("customer_phone may already exist:", e)

        try:
            conn.execute(text("ALTER TABLE `order` ADD COLUMN customer_address VARCHAR(200)"))
            print("customer_address has been added")
        except Exception as e:
            print("customer_address may already exist:", e)

        conn.commit()

print("Database migration is complete; you can now access Order as new fields")
