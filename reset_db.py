import os
from app import app, db

# 默认数据库文件名，可以根据实际情况修改
DB_FILE = "food.db"

with app.app_context():
    # 删除旧数据库文件
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"🗑️ 已删除旧数据库文件: {DB_FILE}")
    else:
        print(f"⚠️ 未找到数据库文件 {DB_FILE}，可能是首次运行")

    # 重新创建所有表
    db.create_all()
    print("✅ 数据库已重建，表结构与最新 models.py 保持一致")
