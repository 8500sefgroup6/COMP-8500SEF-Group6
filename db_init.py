from app import app, db, MenuItem

sample_menu = [
    {
        "name": "Margherita Pizza",
        "description": "Classic tomato, mozzarella, basil",
        "price_cents": 8800,
        "image_url": "images/pizza.jpg"
    },
    {
        "name": "Pepperoni Pizza",
        "description": "Pepperoni, mozzarella, tomato",
        "price_cents": 9800,
        "image_url": "images/pepperoni.jpg"
    },
    {
        "name": "Chicken Katsu Bento",
        "description": "Crispy chicken, rice, salad",
        "price_cents": 10500,
        "image_url": "images/bento.jpg"
    },
    {
        "name": "Sushi Set",
        "description": "Assorted nigiri & rolls",
        "price_cents": 12800,
        "image_url": "images/sushi.jpg"
    },
    {
        "name": "Ramen Tonkotsu",
        "description": "Pork broth, chashu, egg",
        "price_cents": 9200,
        "image_url": "images/ramen.jpg"
    },
    {
        "name": "Curry Rice",
        "description": "Japanese curry with veggies",
        "price_cents": 7800,
        "image_url": "images/curry.jpg"
    },
]

with app.app_context():
    db.create_all()
    if not MenuItem.query.first():
        for m in sample_menu:
            db.session.add(MenuItem(**m))
        db.session.commit()
        print("Database initialized and sample menu with local images inserted.")
    else:
        print("Menu already exists. Nothing to do.")
