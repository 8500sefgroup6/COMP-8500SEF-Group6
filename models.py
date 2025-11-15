from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class OrderStatus(str, Enum):
    placed = "placed"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    price_cents = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255))

    def price(self) -> float:
        return self.price_cents / 100.0

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20))
    customer_address = db.Column(db.String(255))

    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.placed, nullable=False)
    total_cents = db.Column(db.Integer, default=0, nullable=False)

    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")

    def total(self) -> float:
        return self.total_cents / 100.0

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price_cents = db.Column(db.Integer, default=0, nullable=False)

    menu_item = db.relationship("MenuItem")

    def line_total_cents(self) -> int:
        return self.quantity * self.unit_price_cents
