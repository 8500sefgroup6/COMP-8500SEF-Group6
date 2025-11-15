from flask import Flask, render_template, session, redirect, url_for, request, flash
from models import db, MenuItem, Order, OrderItem, OrderStatus
from datetime import timedelta
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-for-class")
app.permanent_session_lifetime = timedelta(hours=6)

db.init_app(app)

def get_cart():
    return session.setdefault("cart", {})  

@app.context_processor
def inject_globals():
    return {"OrderStatus": OrderStatus}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    items = MenuItem.query.order_by(MenuItem.name).all()
    return render_template("menu.html", items=items, cart=get_cart())

@app.route("/add_to_cart/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    item = MenuItem.query.get_or_404(item_id)
    cart = get_cart()
    qty = int(request.form.get("qty", 1))
    cart[str(item_id)] = cart.get(str(item_id), 0) + max(1, qty)
    session["cart"] = cart
    flash(f"Added {qty} × {item.name} to cart.", "success")
    return redirect(url_for("menu"))

@app.route("/remove_from_cart/<int:item_id>", methods=["POST"])
def remove_from_cart(item_id):
    cart = get_cart()
    if str(item_id) in cart:
        cart.pop(str(item_id))
        session["cart"] = cart
        flash("Item removed from cart.", "info")
    else:
        flash("Item not found in cart.", "warning")
    return redirect(url_for("view_cart"))


@app.route("/cart")
def view_cart():
    cart = get_cart()
    ids = [int(i) for i in cart.keys()]
    items = MenuItem.query.filter(MenuItem.id.in_(ids)).all() if ids else []
    lines = []
    subtotal_cents = 0
    for it in items:
        qty = int(cart[str(it.id)])
        line_total = qty * it.price_cents
        subtotal_cents += line_total
        lines.append({"item": it, "qty": qty, "line_total_cents": line_total})
    return render_template("cart.html", lines=lines, subtotal_cents=subtotal_cents)

@app.route("/update_cart", methods=["POST"])
def update_cart():
    cart = {}
    for key, val in request.form.items():
        if key.startswith("qty_"):
            item_id = key.split("_",1)[1]
            try:
                qty = max(0, int(val))
            except:
                qty = 0
            if qty > 0:
                cart[item_id] = qty
    session["cart"] = cart
    flash("Cart updated.", "info")
    return redirect(url_for("view_cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = get_cart()  # dict: { "item_id": qty }
    if not cart:
        flash("Your cart is empty!", "warning")
        return redirect(url_for("menu"))

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        customer_phone = request.form.get("customer_phone", "").strip()
        customer_address = request.form.get("customer_address", "").strip()

        
        if not (customer_name and customer_phone and customer_address):
            flash("Please fill in your name, phone, and address.", "warning")
            return render_template("checkout.html")

        ids = [int(i) for i in cart.keys()]
        items = MenuItem.query.filter(MenuItem.id.in_(ids)).all()
        if not items:
            flash("Your cart is empty!", "warning")
            return redirect(url_for("menu"))

        
        order = Order(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            status=OrderStatus.placed
        )
        db.session.add(order)
        db.session.flush()   

        total_cents = 0
        items_by_id = {it.id: it for it in items}
        for sid, qty in cart.items():
            try:
                it_id = int(sid)
            except:
                continue
            it = items_by_id.get(it_id)
            if not it:
                continue
            q = max(1, int(qty))
            oi = OrderItem(
                order_id=order.id,   
                menu_item_id=it.id,
                quantity=q,
                unit_price_cents=it.price_cents
            )
            db.session.add(oi)
            total_cents += q * it.price_cents

        order.total_cents = total_cents
        db.session.commit()

       
        session["cart"] = {}
        flash("Order placed successfully!", "success")
        return redirect(url_for("my_orders"))

    return render_template("checkout.html")


@app.route("/my_orders")
def my_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("my_orders.html", orders=orders)

@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price_cents = int(float(request.form["price"]) * 100)
        image_url = request.form.get("image_url", "images/default.jpg")

        new_item = MenuItem(name=name, description=description, price_cents=price_cents, image_url=image_url)
        db.session.add(new_item)
        db.session.commit()
        flash(f"Menu item {name} added.", "success")
        return redirect(url_for("admin"))

    return render_template("add_item.html")

@app.route("/order/<int:order_id>")
def track_order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("track_order.html", order=order)

@app.route("/admin/update_status/<int:order_id>", methods=["POST"])
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get("status", "placed")
    try:
        if hasattr(OrderStatus, new_status):
            order.status = OrderStatus[new_status]
        else:
            order.status = OrderStatus(new_status) if 'OrderStatus' in globals() else new_status
        db.session.commit()
        flash(f"Order #{order.id} status updated to {new_status}.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to update status: {e}", "error")
    return redirect(url_for("admin"))

@app.route("/admin/delete_order/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    try:
        OrderItem.query.filter_by(order_id=order.id).delete()
        db.session.delete(order)
        db.session.commit()
        flash(f"Order #{order.id} deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to delete order: {e}", "error")
    return redirect(url_for("admin"))

@app.route("/delete_item/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f"Menu item {item.name} deleted.", "info")
    return redirect(url_for("admin"))

@app.route("/order/<int:order_id>")
def order_status(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("order_status.html", order=order)

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        order_id = int(request.form.get("order_id"))
        new_status = request.form.get("status")
        order = Order.query.get_or_404(order_id)
        if new_status in [s.value for s in OrderStatus]:
            order.status = OrderStatus(new_status)
            db.session.commit()
            flash(f"Order #{order.id} status updated to {order.status}.", "success")
        else:
            flash("Invalid status.", "danger")
        return redirect(url_for("admin"))

    items = MenuItem.query.order_by(MenuItem.name).all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin.html", items=items, orders=orders)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
