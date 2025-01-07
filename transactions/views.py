from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin

from .forms import TransactionForm, EntryFormSet, EntryFormSet_update
from .mixins import TransactionFormValidator
from .models import Transaction, Entry

class GetListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "journals/transaction_list.html"
    
class PostListView(LoginRequiredMixin, FormMixin, ListView):
    model = Transaction
    template_name = "journals/search_results.html"
    
    def get_queryset(self):
        query = self.request.POST.get("keyword")
        return Transaction.objects.filter(
            Q(description__icontains=query)| Q(slug__icontains=query) | Q(shop__icontains=query)
        )

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class TransactionListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = GetListView.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = PostListView.as_view()
        return view(request, *args, **kwargs)

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
