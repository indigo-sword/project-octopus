import requests
from uuid import uuid4
import random
import string
import sys

port = sys.argv[1]
url = f'http://localhost:{port}/'

def random_email():
       return ''.join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"

def test_base_get():
    response = requests.get(url)
    print(response.json())

def test_base_post():
    response = requests.post(url, data={
        "key1": "value1",
        "key2": "value2",
    
    })
    print(response.json())

def test_create_user():
    response = requests.post(url + "create_user", data={
        "username": uuid4(),
        "password": "password_4_joao",
        "email": random_email(),
    })

    print(response.json())

def test_base():
    test_base_get()
    test_base_post()

def main():
    test_base()
    test_create_user()

if __name__ == "__main__":
    main()