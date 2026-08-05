import random
import string
from faker import Faker


class RandomDataUtil:

    def __init__(self):
        self.faker = Faker()
        self.random = random

    def get_first_name(self) -> str:
        return self.faker.first_name()

    def get_last_name(self) -> str:
        return self.faker.last_name()

    def get_address(self) -> str:
        return self.faker.address().replace("\n", " ")

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
        # Generates a fresh unique username like 'john_4829' every time
        return f"{self.faker.user_name()}_{self.random.randint(1000, 9999)}"

    def get_random_password(self) -> str:
        return "Pass123!"

    def get_random_amount(self) -> str:
        return str(self.faker.random_number(digits=3))