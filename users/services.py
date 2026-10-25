from config.settings import STRIPE_SECRET_KEY
import stripe

client = stripe.StripeClient(STRIPE_SECRET_KEY)


def create_stripe_price(amount, course_name):
    """Функция создает цену продукта."""

    price = client.v1.prices.create(
        params = {
            "currency": "rub",
            "unit_amount": int(amount * 100),
            "product_data": { "name": course_name },
        }
    )
    return price

def create_stripe_session(price):

    session = client.v1.checkout.sessions.create(
        params = {
        "success_url": "https://127.0.0.1:8000/",
        "line_items": [{ "price": price.id, "quantity": 1 }],
        "mode": "payment",
        }
    )

    return session.id, session.url