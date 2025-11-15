from app import app, db
from sqlalchemy import text

# 必须进入 app context 才能使用 db.engine
with app.app_context():
    with db.engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE `order` ADD COLUMN customer_name VARCHAR(80)"))
            print("✅ customer_name 字段已添加")
        except Exception as e:
            print("⚠️ customer_name 字段可能已存在:", e)

        try:
            conn.execute(text("ALTER TABLE `order` ADD COLUMN customer_phone VARCHAR(20)"))
            print("✅ customer_phone 字段已添加")
        except Exception as e:
            print("⚠️ customer_phone 字段可能已存在:", e)

        try:
            conn.execute(text("ALTER TABLE `order` ADD COLUMN customer_address VARCHAR(200)"))
            print("✅ customer_address 字段已添加")
        except Exception as e:
            print("⚠️ customer_address 字段可能已存在:", e)

        conn.commit()

print("🎉 数据库迁移完成，可以在 Order 表使用新字段了")
