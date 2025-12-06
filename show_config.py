from app import app

def show_config():
    uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    print(f"SQLALCHEMY_DATABASE_URI = {uri}")

if __name__ == "__main__":
    show_config()
