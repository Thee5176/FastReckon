from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import JournalRecord

class ListRecordView(ListView):
    model = JournalRecord
    template_name = "journals/list_record.html"

class ListRecordView(DetailView):
    model = JournalRecord
    template_name = "journals/detail_record.html"


class CreateRecordView(CreateView):
    model = JournalRecord
    template_name = 'journals/create_record.html'
    fields = '__all__'