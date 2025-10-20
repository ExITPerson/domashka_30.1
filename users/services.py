import stripe
import os
from django.urls import reverse
from dotenv import load_dotenv


load_dotenv(override=True)


class CreatePayment:
    stripe.api_key = os.getenv('API_KEY_STRIPE')

    def __create_product(self, name, description):
        try:
            product = stripe.Product.create(
                name=name,
                description=description,
            )

            return product
        except stripe._error.StripeError as e:
            raise e

    def __create_price(self, payment_amount, product):
        try:
            price = stripe.Price.create(
                product=product.id,
                unit_amount=payment_amount,
                currency='rub'
            )
            return price
        except stripe._error.StripeError as e:
            raise e

    def __create_payment_session(self, price):
        try:
            session = stripe.checkout.Session.create(
                line_items=[{'price': str(price.id), 'quantity': 1}],
                mode="payment",
                success_url='http://127.0.0.1:8000/' + reverse('users:payments'),
                cancel_url='http://127.0.0.1:8000/' + reverse('users:payments'),

            )
            return session
        except stripe._error.StripeError as e:
            raise e


    def get_payment_link(self, name, description, payment_amount):
        try:
            product = self.__create_product(name, description)
            price = self.__create_price(payment_amount, product)
            session = self.__create_payment_session(price)

            return session
        except stripe._error.StripeError as e:
            raise e
