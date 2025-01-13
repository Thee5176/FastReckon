
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView

from .models import Account, AccountLevel1, AccountLevel2, AccountLevel3
from .mixins import AccountColorCodeMixin, UserOwnedQuerysetMixin
from transactions.models import Transaction

class AccountListView(AccountColorCodeMixin, UserOwnedQuerysetMixin, ListView):
    model = Account
    template_name = "acc_codes/account_list.html"      

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        code = self.request.GET.get("code")
        
        if name:
            queryset = queryset.filter(name__icontains=name)
              
        if code:
            queryset = queryset.filter(code__startswith=code)
            
        return queryset   
    
class AccountDetailView(LoginRequiredMixin, AccountColorCodeMixin, UserOwnedQuerysetMixin, DetailView):
    model = Account
    template_name = "acc_codes/account_detail.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("level3__level2__level1")
        return queryset    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        obj = self.get_object()
        if obj:
            context["transaction_list"] = Transaction.objects.filter(entries__code=obj)
        return context
    
    
class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    template_name = "acc_codes/account_alter_form.html"
    fields = ["name","level3","sub_account","detailed_account","guideline"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Create"
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Account
    template_name = "acc_codes/account_alter_form.html"
    fields = ["name","level3","sub_account","detailed_account","guideline"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Update"
        return context
    
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    template_name = "journals/account_delete.html"
    success_url = reverse_lazy("account_list")

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user