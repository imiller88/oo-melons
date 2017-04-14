"""Classes for melon orders."""
import random
import datetime

class TooManyMelonsError(ValueError):
    def __init__(self):
        super(TooManyMelonsError, self).__init__("No more than 100 melons!")
    pass

class AbstractMelonOrder(object):
    tax = 0
    order_type = None

    def __init__(self, species, qty):
        """Initialize melon order attributes."""

        self.species = species
        self.qty = qty
        self.shipped = False
        self.base_price = self.set_base_price()

        if self.qty > 100:
            raise TooManyMelonsError()

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True

    def set_base_price(self):
        """ determines base price """
        base_price = random.randint(5,9)
        now = datetime.datetime.now()

        if 8 <= now.hour < 11 and 0 <= now.weekday() <= 4:
            # adds $4 during rush hour (8-11) on weekdays
            base_price += 4

        return base_price

    def get_total(self):
        """Calculate price, including tax."""

        base_price = self.base_price()

        if self.species == "christmas":
            base_price *= 1.5

        total = (1 + self.tax) * self.qty * base_price

        if self.order_type == "international" and self.qty < 10:
            total += 3

        return total

class GovernmentMelonOrder(AbstractMelonOrder):
    """A melon order from the US Govt"""
    passed_inspection = False

    def mark_inspection(self, passed):
        self.passed_inspection = passed

class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""
    order_type = "domestic"
    tax = 0.08


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""
    order_type = "international"
    tax = 0.17

    def __init__(self, species, qty, country_code):
        """Initialize melon order attributes."""

        super(InternationalMelonOrder, self).__init__(species, qty)
        self.country_code = country_code


    def get_country_code(self):
        """Return the country code."""

        return self.country_code

