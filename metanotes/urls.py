from django.urls import path

from .views import GetNotesView, AddNoteView, RemoveNoteView

app_name = 'metanotes'

urlpatterns = [
    path('get/', GetNotesView.as_view(), name='get'),
    path('add/', AddNoteView.as_view(), name='add'),
    path('remove/', RemoveNoteView.as_view(), name='remove'),
]
