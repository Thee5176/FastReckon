from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from datetime import datetime

from .forms import TransactionForm, EntryFormSet, EntryFormSet_update
from .mixins import TransactionFormValidator
from .models import Transaction, Entry
from acc_codes.mixins import UserOwnedQuerysetMixin

class TransactionListView(LoginRequiredMixin, UserOwnedQuerysetMixin, ListView):
    model = Transaction
    template_name = "transactions/transaction_list.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        kw = self.request.GET.get("keyword")
        date = self.request.GET.get("created")
        
        if kw:
            queryset = queryset.filter(Q(description__icontains=kw)| Q(slug__icontains=kw) | Q(shop__icontains=kw))
            
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(created__date=date_obj)
                print(f"Filtering by date: {date_obj}")
            except ValueError:
                print(f"Invalid date format: {date}")
                
        return queryset    

class TransactionDetailView(LoginRequiredMixin, UserOwnedQuerysetMixin, DetailView):
    model = Transaction
    template_name = "transactions/transaction_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = self.get_object()
        context["entries"] = Entry.objects.select_related('transaction','code__level3__level2__level1').filter(transaction_id=transaction.id)
        return context

class TransactionCreateView(LoginRequiredMixin, TransactionFormValidator, FormView):
    form_class = TransactionForm        
    success_url = reverse_lazy("transaction_list")    
    template_name = "transactions/transaction_alter_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry_formset"] = EntryFormSet(queryset=Entry.objects.none())
        context["view_name"] = "Create"
        return context
        
class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, TransactionFormValidator, FormView):
    form_class = TransactionForm
    success_url = reverse_lazy("transaction_list")    
    template_name = "transactions/transaction_alter_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = self.get_object()
        context["entry_formset"] = EntryFormSet_update(queryset=Entry.objects.select_related('transaction').filter(transaction=transaction))
        context["view_name"] = "Update"
        return context
    
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user
    

class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    template_name = "transactions/transaction_delete.html"
    success_url = reverse_lazy("transaction_list")
    
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user
