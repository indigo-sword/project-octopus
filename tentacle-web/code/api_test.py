import requests
from uuid import uuid4
import random
import string

url = 'http://localhost:7809/'  # Replace with the actual URL and port of your Flask app

# Data to be sent in the POST request
data = {
    'key1': 'value1',
    'key2': 'value2'
}

def random_email():
       return ''.join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"

def test_base_get():
    response = requests.get(url)
    print(response.json())

def test_base_post():
    response = requests.post(url, data=data)
    print(response.json())

def test_create_user():
    response = requests.post(url + "create_user", data={
        "username": uuid4(),
        "password": "password_4_joao",
        "email": random_email(),
    })

def test_base():
    test_base_get()
    test_base_post()

def main():
    test_base()
    test_create_user

if __name__ == "__main__":
    main()