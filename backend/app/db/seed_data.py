from sqlalchemy.orm import Session

from app.models.db_models import Product, Order, FAQ


def seed_database(db: Session):
    if db.query(Product).count() == 0:
        products = [
            Product(name="Sugar 1kg", price=55.0, stock=100, category="grocery"),
            Product(name="Rice 5kg", price=320.0, stock=40, category="grocery"),
            Product(name="Milk 1L", price=60.0, stock=80, category="dairy"),
            Product(name="Cooking Oil 1L", price=150.0, stock=30, category="grocery"),
        ]
        db.add_all(products)

    if db.query(Order).count() == 0:
        orders = [
            Order(order_id="ORD1001", customer_name="Test Customer", status="shipped", items="Sugar 1kg, Milk 1L"),
            Order(order_id="ORD1002", customer_name="Another Customer", status="placed", items="Rice 5kg"),
        ]
        db.add_all(orders)

    if db.query(FAQ).count() == 0:
        faqs = [
            FAQ(question="What are your shop timings?", answer="Shop khulta hai 9 AM se 9 PM tak, sab din.", category="store_hours"),
            FAQ(question="Do you deliver?", answer="Haan, hum 5km radius mein free delivery dete hain.", category="delivery"),
            FAQ(question="What is your return policy?", answer="Aap 7 din ke andar product return kar sakte hain bill ke saath.", category="return_policy"),
        ]
        db.add_all(faqs)

    db.commit()