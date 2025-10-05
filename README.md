# Food Ordering & Tracking App (Flask + SQLite)

A compact teaching-ready web app demonstrating a food ordering workflow with live order tracking and an admin dashboard.

## Features
- Browse menu, add to cart, checkout
- Order confirmation with tracking page (`/order/<id>`)
- Order statuses: `placed → preparing → out_for_delivery → delivered → cancelled`
- Admin dashboard to update order status
- SQLite database (auto-created)
- Simple session cart (no auth to keep it course-friendly)

## Quickstart

```bash
# 1) Create a virtualenv (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Initialize DB and sample menu
python db_init.py

# 4) Run the app
python app.py
# Then open http://127.0.0.1:5000
```

## Admin
- Visit `/admin` to see orders and update status.

## Project Structure
```
food_ordering_app/
  app.py
  models.py
  db_init.py
  requirements.txt
  templates/
    base.html
    index.html
    menu.html
    cart.html
    checkout.html
    order_status.html
    admin.html
  static/
    style.css
```

## Notes
- This is intentionally minimal. You can extend with user accounts, payments, delivery ETA, WebSocket updates, etc.
- For demo, the "address" and "phone" are collected at checkout and stored per order.
