from src.core import auth
def run():
    Luca = auth.create_user(email="luca@mail.com", password="123456")
    Franco = auth.create_user(email="franco@mail.com", password="123456")
    Messi = auth.create_user(email="messi@mail.com", password="123456")
