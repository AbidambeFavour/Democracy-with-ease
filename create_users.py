#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplevote.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Create regular users
users_data = [
    {'username': 'john_doe', 'email': 'john@example.com', 'password': 'user123', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'user123', 'first_name': 'Jane', 'last_name': 'Smith'},
    {'username': 'bob_wilson', 'email': 'bob@example.com', 'password': 'user123', 'first_name': 'Bob', 'last_name': 'Wilson'},
    {'username': 'alice_brown', 'email': 'alice@example.com', 'password': 'user123', 'first_name': 'Alice', 'last_name': 'Brown'},
    {'username': 'charlie_davis', 'email': 'charlie@example.com', 'password': 'user123', 'first_name': 'Charlie', 'last_name': 'Davis'}
]

for user_data in users_data:
    if not User.objects.filter(username=user_data['username']).exists():
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        print(f'Created user: {user_data["username"]}')
    else:
        print(f'User {user_data["username"]} already exists')

print('User creation completed!')
