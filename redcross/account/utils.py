# utils.py

from django.contrib.auth.models import User
import random
import string
from datetime import datetime

def generate_user_id():
    # Get the last 2 digits of the current year
    current_year = datetime.now().year % 100
    # Generate a random 5-character alphanumeric string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    # Combine the two parts to form the user ID
    user_id = f"{current_year}-{random_string}"
    # Check if the user ID already exists in the database
    while User.objects.filter(username=user_id).exists():
        # If it does, generate a new one
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        user_id = f"{current_year}-{random_string}"
    return user_id
