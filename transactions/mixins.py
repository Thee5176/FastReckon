from .forms import TransactionForm, EntryFormSet
from .models import Transaction

class BalanceValidator:
    """Check if the list of 'entries' (context_name) are Dr/Cr balanced."""
    def __init__(self,entries):
        self.entries = entries

    @property    
    def total_debits(self):
        return sum(entry.amount for entry in self.entries if entry.entry_type == 1)
    
    @property
    def total_credits(self):
        return sum(entry.amount for entry in self.entries if entry.entry_type == 2)

    def check_balance(self):
        return self.total_debits == self.total_credits

class TransactionFormValidator:
    """
    Form Checklist:
    - Dr/Cr Balance
    - Assign intra-month-ref
    Form Auto-filled:
    - Transaction.created_by = self.get_object().user
    - Entry.transaction = self.get_object()
    """
    
    def form_valid(self, form):
        """
        Add validation for additional form context: EntryFormSet
        """
        transaction = form.save(commit=False)
        formset = EntryFormSet(self.request.POST)

        if formset.is_valid():
            entries = formset.save(commit=False)
            MyBalance = BalanceValidator(entries)
            
            print(MyBalance.total_debits)
            print(MyBalance.total_credits)
            
            if not MyBalance.check_balance():
                formset.non_form_errors().append(f"Amount is invalid. - Dr/Cr Amount :{MyBalance.total_debits}/{MyBalance.total_credits}")
                print("Entry fields has invalid value")
                return self.render_to_response(
                    self.get_context_data(form=form, formset=formset)
                )
            #Assign User before save transaction
            transaction.created_by = self.request.user
            transaction.save()
            
            #Assign transaction before save to entries
            try:
                for entry in entries:
                    entry.transaction = transaction
                    entry.save()
            except Exception as e:
                print("Error saving entry:", e)
        
        return super().form_valid(form)
        
                
    def form_invalid(self, form):
        """
        Add validation for additional form context: EntryFormSet
        """
        formset = EntryFormset(self.request.POST)
        print("Transaction Form is invalid")
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )
