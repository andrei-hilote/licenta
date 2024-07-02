# populate_temperature_data.py
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meteo_app.settings')  # Schimbă 'myproject.settings' cu calea corectă

import django

django.setup()

import random
from faker import Faker
from django.utils import timezone
from dashboard.models import Temperature

fake = Faker()


def generate_mock_data(num_entries):
    mock_data = []
    for _ in range(num_entries):
        temp_type = random.choice(['outside', 'inside'])
        temperature = random.uniform(-10.0, 40.0)  # Generăm o temperatură aleatoare între -10.0 și 40.0
        date = fake.date_time_between(start_date='-30d',
                                      end_date='now')  # Generăm o dată aleatoare în ultimele 30 de zile
        mock_data.append({'type': temp_type, 'temperature': temperature, 'date': date})
    return mock_data


def populate_data():
    mock_data = generate_mock_data(20)  # Generăm 20 de înregistrări fictive

    for data in mock_data:
        temperature_obj = Temperature(type=data['type'], temperature=data['temperature'], date=data['date'])
        temperature_obj.save()
        print(f"Adăugată înregistrare de temperatură: {temperature_obj}")


if __name__ == "__main__":
    populate_data()
