import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAULTS_FILE = os.path.join(PROJECT_ROOT, 'faults_database.json')
CARS_FILE = os.path.join(PROJECT_ROOT, 'car_brands.json')

def load_faults():
    with open(FAULTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)['faults_database']

def load_cars():
    with open(CARS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)['car_brands']

