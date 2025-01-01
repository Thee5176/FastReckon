
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView

from .models import Account
#BOOK

#ACCOUNT
class AccountListView(ListView):
    model = Account
    template_name = "acc_codes/account_list.html"

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = "acc_codes/account_detail.html"
    
class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    template_name = "acc_codes/account_alter_form.html"
    fields = ["name","super_account","sub_account","detailed_account","guideline"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "CREATE"
        return context
    
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Account
    template_name = "acc_codes/account_alter_form.html"
    fields = ["name","super_account","sub_account","detailed_account","guideline"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "UPDATE"
        return context
    
    def test_func(self):
        self.request.user = self.request.object

class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    template_name = "journals/account_delete.html"
    success_url = reverse_lazy("account_list")

    def test_func(self):
        self.request.user = self.request.object


#TRANSACTION
