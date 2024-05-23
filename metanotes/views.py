from datetime import datetime
from urllib.parse import urlparse

from django.conf import settings
from django.http import JsonResponse
from django.urls import resolve
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from metanotes import utils


@method_decorator(csrf_exempt, name='dispatch')
class GetNotesView(View):
    def get(self, request):
        referrer_view_name = utils.get_referrer_view_name(request)

        notes_data = utils.get_notes_data()

        notes = [note for note in notes_data['notes'] if note['view'] == referrer_view_name]

        return JsonResponse(notes, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class AddNoteView(View):
    def post(self, request):
        data = json.loads(request.body)
        # view name with namespace
        referrer_view_name = utils.get_referrer_view_name(request)
        content = data.get('content')
        author = request.user.email
        timestamp = datetime.now().isoformat()

        notes_data = utils.get_notes_data()

        notes_data['notes'].append({
            'uuid': str(uuid.uuid4()),
            'view': referrer_view_name,
            'content': content,
            'author': author,
            'timestamp': timestamp
        })

        utils.save_notes_data(notes_data)

        return JsonResponse({'status': 'success'})


@method_decorator(csrf_exempt, name='dispatch')
class RemoveNoteView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        note_id = data.get('id')

        notes_data = utils.get_notes_data()

        notes_data['notes'] = [note for note in notes_data['notes'] if note['uuid'] != note_id]

        utils.save_notes_data(notes_data)

        return JsonResponse({'status': 'success'})