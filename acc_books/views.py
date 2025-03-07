from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Book
from accounts.mixins import UserOwnedQuerysetMixin

class BookListView(LoginRequiredMixin, UserOwnedQuerysetMixin, ListView):
    model = Book
    templates_name = "acc_books/book_list.html"
    
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ["name","abbr","guideline","currency_sign"]
    template_name = "acc_books/book_alter_form.html"
    success_url = reverse_lazy("book_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Create"
        return context
    
class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    fields = ["name","abbr","guideline"]
    template_name = "acc_books/book_alter_form.html"
    success_url = reverse_lazy("book_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Update"
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = self.request.user
            book = form.save()
        return super().form_valid(form)
    
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = "acc_books/book_delete.html"
    success_url = reverse_lazy("book_list")

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user