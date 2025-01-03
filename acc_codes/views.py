
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView

from .models import Account, AccountLevel1, AccountLevel2, AccountLevel3
from .mixins import AccountColorCodeMixin

class AccountListView(AccountColorCodeMixin, ListView):
    model = Account
    template_name = "acc_codes/account_list.html"    

class AccountDetailView(LoginRequiredMixin, AccountColorCodeMixin, DetailView):
    model = Account
    template_name = "acc_codes/account_detail.html"
    
    def get_chart_of_account(self, search_code):
        return AccountLevel1.objects.filter(code=search_code[0])
    
    def get_account_type(self, search_code):
        return AccountLevel2.objects.filter(code=search_code[:2])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        obj = self.get_object()
        if obj:
            obj_code = obj.code
            context["chart_of_account"] = self.get_chart_of_account(obj_code)
            context["account_type"] = self.get_account_type(obj_code)
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