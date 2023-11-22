from faker import Faker

fake = Faker()


def create_fake_user():
    email = fake.email()
    password = fake.password(length=12)
    return {
        "email": email,
        "password": password,
    }
