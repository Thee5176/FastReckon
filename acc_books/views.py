from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Book
from acc_codes.mixins import UserOwnedQuerysetMixin

class BookListView(LoginRequiredMixin, UserOwnedQuerysetMixin, ListView):
    model = Book
    templates_name = "acc_books/book_list.html"
    
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = "acc_books/book_alter_form.html"
    fields = "__all__"
    success_url = reverse_lazy("book_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Create"
        return context
    
class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    template_name = "acc_books/book_alter_form.html"
    fields = "__all__"
    success_url = reverse_lazy("book_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Update"
        return context
    
    def test_func(self):
        obj = self.get_object()
        return obj.recorder == self.request.user

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = "acc_books/book_delete.html"
    success_url = reverse_lazy("book_list")

    def test_func(self):
        obj = self.get_object()
        return obj.recorder == self.request.user