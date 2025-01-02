from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Book

class BookListView(ListView):
    model = Book
    templates_name = "acc_books/book_list.html"

class BookCreateView(CreateView):
    model = Book
    template_name = "acc_books/book_alter_form.html"
    fields = "__all__"
    success_url = reverse_lazy("book_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Create"
        return context
    
class BookUpdateView(UpdateView):
    model = Book
    template_name = "acc_books/book_alter_form.html"
    fields = "__all__"
    success_url = reverse_lazy("book_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Update"
        return context

class BookDeleteView(DeleteView):
    model = Book
    template_name = "acc_books/book_delete.html"
    success_url = reverse_lazy("book_list")