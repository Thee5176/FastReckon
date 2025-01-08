from django.views.generic import View
from django.db.models import QuerySet

class UserOwnedQuerysetMixin:
    """
    A mixin to add filter to get only objects owned by the current user
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        if isinstance(queryset, QuerySet):
            return queryset.filter(created_by=self.request.user)
        return queryset

class AccountColorCodeMixin(View):
    color_by_code = ["dark","primary","success","danger","warning","info"]
    
    def add_query_color_code(self, queryset):
        """
        Add `color_code` attribute to each object in queryset based on attribute `code`
        """
        for obj in queryset:
            try:
                obj.color_code = self.color_by_code[int(obj.code[0])]
            except(IndexError, ValueError):
                obj.color_code = self.color_by_code[0]
        return queryset
    
    def add_obj_color_code(self, obj):
        """
        Add `color_code` attribute to each object in queryset based on attribute `code`
        """
        if obj:
            try:
                obj.color_code = self.color_by_code[int(obj.code[0])]
            except(IndexError, ValueError):
                obj.color_code = self.color_by_code[0]
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'object' in context:         #DetailView, UpdateView
            context['object'] = self.add_obj_color_code(context['object'])
        elif 'account_list' in context: #ListView
            context['account_list'] = self.add_query_color_code(context['account_list'])
        elif 'queryset' in context:
            context['queryset'] = self.add_query_color_code(context['queryset'])
        
        return context