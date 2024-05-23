import json
from urllib.parse import urlparse

from django.conf import settings
from django.urls import resolve
import os


def get_notes_file_path():
    path = getattr(settings, 'METANOTES_PATH', getattr(settings, 'BASE_DIR'))
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            json.dump({'notes': []}, file, indent=4)
    return path


def get_referrer_view_name(request):
    url = urlparse(request.META.get('HTTP_REFERER', '')).path
    view_name = resolve(url).view_name
    return view_name


def get_notes_data():
    with open(get_notes_file_path(), 'r') as file:
        notes_data = json.load(file)
    return notes_data

def save_notes_data(notes_data):
    with open(get_notes_file_path(), 'w') as file:
        json.dump(notes_data, file)