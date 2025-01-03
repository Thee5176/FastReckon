from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Transaction

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "journals/transaction_list.html"

class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "journals/transaction_detail.html"

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = "journals/transaction_alter_form.html"
    fields = ["book", "description", "date"]
    
    def form_valid(self, form):
        # auto add user
        form.instance.recorder = self.request.user
        # validate dr/cr
        if form.instance.is_balanced:
            return super().form_valid(form)
        else:
            raise ValueError("Invalid: Transaction Imbalanced")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Create"
        return context
    

class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    template_name = "journals/transaction_alter_form.html"
    fields = ["book", "description", "date"]
    
    def test_func(self):
        obj = self.get_object()
        return obj.recorder == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Update"
        return context
    

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = "journals/transaction_delete.html"
    success_url = reverse_lazy("")
