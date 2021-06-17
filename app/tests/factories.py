from datetime import timedelta, timezone
from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from app.models import (
    Announcement,
    Category,
    DeliverySpeed,
    District,
    Location,
    Order,
    OrderItem,
    Payment,
    Product,
    Shop,
    Stock,
    User,
)

faker = Factory.create()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    dob = LazyFunction(faker.date)
    verified = LazyFunction(faker.boolean)
    phone = LazyAttribute(lambda o: faker.text(max_nb_chars=15))
    role = fuzzy.FuzzyChoice(User.ROLE_CHOICES, getter=lambda c: c[0])


class UserWithForeignFactory(UserFactory):
    @factory.post_generation
    def payments(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                PaymentFactory(customer=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                PaymentFactory(customer=obj)

    @factory.post_generation
    def orders(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                OrderFactory(driver=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                OrderFactory(driver=obj)


class DistrictFactory(DjangoModelFactory):
    class Meta:
        model = District

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=50))


class DistrictWithForeignFactory(DistrictFactory):
    @factory.post_generation
    def locations(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                LocationFactory(district=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                LocationFactory(district=obj)


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location

    lat = LazyAttribute(lambda o: uniform(0.0, 50.0))
    lng = LazyAttribute(lambda o: uniform(0.0, 50.0))


class LocationWithForeignFactory(LocationFactory):
    @factory.post_generation
    def users(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                UserFactory(location=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                UserFactory(location=obj)

    @factory.post_generation
    def orders(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                OrderFactory(location=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                OrderFactory(location=obj)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    description = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    image = LazyAttribute(lambda o: faker.text(max_nb_chars=255))


class CategoryWithForeignFactory(CategoryFactory):
    @factory.post_generation
    def products(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                ProductFactory(category=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                ProductFactory(category=obj)


class StockFactory(DjangoModelFactory):
    class Meta:
        model = Stock

    product = factory.SubFactory('app.tests.factories.ProductFactory')
    units_in_stock = LazyAttribute(lambda o: randint(0, 10000))
    units_on_order = LazyAttribute(lambda o: randint(0, 10000))
    created_at = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))


class ShopFactory(DjangoModelFactory):
    class Meta:
        model = Shop

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    is_special = LazyFunction(faker.boolean)


class ShopWithForeignFactory(ShopFactory):
    @factory.post_generation
    def products(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                ProductFactory(shop=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                ProductFactory(shop=obj)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory('app.tests.factories.CategoryFactory')
    shop = factory.SubFactory('app.tests.factories.ShopFactory')
    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    expiry_date = LazyAttribute(lambda o: faker.date_time(
        tzinfo=timezone(timedelta(0))).isoformat())
    weight = LazyAttribute(lambda o: uniform(0.0, 10000))
    image = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    discount = LazyAttribute(lambda o: randint(0, 99))
    description = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    color = LazyAttribute(lambda o: faker.text(max_nb_chars=50))
    price = LazyAttribute(lambda o: randint(500, 10000))


class ProductWithForeignFactory(ProductFactory):
    @factory.post_generation
    def stocks(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                StockFactory(product=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                StockFactory(product=obj)

    @factory.post_generation
    def orderitems(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                OrderItemFactory(product=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                OrderItemFactory(product=obj)


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    customer = factory.SubFactory('app.tests.factories.UserFactory')
    order = factory.SubFactory('app.tests.factories.OrderFactory')
    created_at = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    paid_at = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    amount = LazyAttribute(lambda o: randint(500, 10000))
    status = fuzzy.FuzzyChoice(Payment.STATUS_CHOICES, getter=lambda c: c[0])


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    location = factory.SubFactory('app.tests.factories.LocationFactory')
    deliveryspeed = factory.SubFactory('app.tests.factories.DeliverySpeedFactory')
    created_at = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    status = fuzzy.FuzzyChoice(Order.STATUS_CHOICES, getter=lambda c: c[0])
    valid = LazyFunction(faker.boolean)
    delivery_method = fuzzy.FuzzyChoice(Order.DELIVERY_METHOD_CHOICES, getter=lambda c: c[0])
    expected_delivery_date_time = LazyAttribute(
        lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    delivery_date_time = LazyAttribute(lambda o: faker.date_time(
        tzinfo=timezone(timedelta(0))).isoformat())
    total_amount = LazyAttribute(lambda o: randint(500, 10000))


class OrderWithForeignFactory(OrderFactory):
    @factory.post_generation
    def payments(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                PaymentFactory(order=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                PaymentFactory(order=obj)


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory('app.tests.factories.ProductFactory')
    units = LazyAttribute(lambda o: randint(1, 10000))
    valid = LazyFunction(faker.boolean)


class DeliverySpeedFactory(DjangoModelFactory):
    class Meta:
        model = DeliverySpeed

    type = fuzzy.FuzzyChoice(DeliverySpeed.TYPE_CHOICES, getter=lambda c: c[0])
    description = LazyAttribute(lambda o: faker.text(max_nb_chars=255))


class DeliverySpeedWithForeignFactory(DeliverySpeedFactory):
    @factory.post_generation
    def orders(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                OrderFactory(deliveryspeed=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                OrderFactory(deliveryspeed=obj)


class AnnouncementFactory(DjangoModelFactory):
    class Meta:
        model = Announcement

    title = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    body = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    image = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
