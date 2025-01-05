from django import forms
from django.forms import modelformset_factory

from .models import Transaction, Entry

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["date","book","description","has_receipt"]
        widgets = {
            'date': forms.TextInput(attrs={'class':'datepicker'})
        }
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["code","entry_type", "amount"]

EntryFormSet = modelformset_factory(Entry, form=EntryForm, extra=2)