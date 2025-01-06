from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import TransactionForm, EntryFormSet, EntryFormSet_update
from .mixins import TransactionFormValidator
from .models import Transaction, Entry

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "journals/transaction_list.html"
    
class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "journals/transaction_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = self.get_object()
        context["entries"] = Entry.objects.filter(transaction_id=transaction.id)
        return context

class TransactionCreateView(LoginRequiredMixin, TransactionFormValidator, FormView):
    form_class = TransactionForm        
    success_url = reverse_lazy("transaction_list")    
    template_name = "journals/transaction_alter_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry_formset"] = EntryFormSet(queryset=Entry.objects.none())
        context["view_name"] = "Create"
        return context
        
class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, TransactionFormValidator, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "journals/transaction_alter_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = self.get_object()
        context["entry_formset"] = EntryFormSet_update(queryset=Entry.objects.filter(transaction=transaction))
        context["view_name"] = "Update"
        return context
    
    def test_func(self):
        obj = self.get_object()
        return obj.recorder == self.request.user
    

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = "journals/transaction_delete.html"
    success_url = reverse_lazy("transaction_list")
