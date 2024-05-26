import json
import os
from urllib.parse import urlparse

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.template.loader import render_to_string
from django.urls import resolve
from datetime import datetime
from django.http import JsonResponse

NOTES_FILE = getattr(settings, "METANOTES_PATH")

if not os.path.exists(NOTES_FILE):
    os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
    with open(NOTES_FILE, "w") as file:
        json.dump({"notes": []}, file, indent=4)


class MetaNotesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated and response.status_code == 200 and 'text/html' in response.get('Content-Type', ''):
            current_view = resolve(request.path_info).view_name
            overlay_html = render_to_string(
                "metanotes/djmn-overlay.html", {"view_name": current_view}
            )
            response.content = response.content.replace(
                b"</body>", overlay_html.encode() + b"</body>"
            )
        return response