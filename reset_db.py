import os
from app import app, db

DB_FILE = "food.db"

with app.app_context():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"🗑️ 已删除旧数据库文件: {DB_FILE}")
    else:
        print(f"⚠️ 未找到数据库文件 {DB_FILE}，可能是首次运行")

    db.create_all()
    print("✅ 数据库已重建，表结构与最新 models.py 保持一致")
