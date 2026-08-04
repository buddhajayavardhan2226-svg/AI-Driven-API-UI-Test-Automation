import random
import string
from faker import Faker


class RandomDataUtil:

    def __init__(self):
        self.faker = Faker()
        # Fix 1: Assign the imported random module directly
        self.random = random

    def get_first_name(self) -> str:
        return self.faker.first_name()

    def get_last_name(self) -> str:
        return self.faker.last_name()

    def get_address(self) -> str:
        return self.faker.address()

    def get_city(self) -> str:
        return self.faker.city()

    def get_state(self) -> str:
        return self.faker.state()

    def get_zipcode(self) -> str:
        return self.faker.zipcode()

    def get_phone(self) -> str:
        return self.faker.phone_number()

    def get_ssn(self) -> str:
        return self.faker.ssn()

    def get_username(self) -> str:
        return self.faker.user_name()

    def get_random_password(self) -> str:
        return self.faker.password(length=8)

    def get_random_amount(self) -> str:
        # Convert to string to prevent Playwright fill errors
        return str(self.faker.random_number(digits=3))

    # def get_random_fromID(self) -> str:
    #     id = self.random.choice(("12345", "12456", "12567", "12678"))
    #     return id
    #
    # def get_random_toId(self) -> str:
    #     id = self.random.choice(("13011", "13122", "13233", "13344"))
        return id