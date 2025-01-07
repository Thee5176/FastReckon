from .forms import TransactionForm, EntryFormSet
from .models import Transaction

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
            
            if self.check_balanced(entries) == False:
                formset.non_form_errors().append("Amount is invalid.")
                print("Entry fields has invalid value")
                return self.render_to_response(
                    self.get_context_data(form=form, formset=formset)
                )
            #Assign User before save transaction
            transaction.recorder = self.request.user
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
    
    def check_balanced(self, entries):
        """Check if the list of 'entries' (imported context) are Dr/Cr balanced."""
        total_debits = sum(entry.amount for entry in entries if entry.entry_type == 1)
        total_credits = sum(entry.amount for entry in entries if entry.entry_type == 2)
        return total_debits == total_credits