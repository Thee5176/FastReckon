from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from journals.models import Transaction, Entry
from acc_codes.models import Account, AccountLevel3
from acc_books.models import Book

class TestCreateTransaction(TestCase):
    def setUp(self):
        # create user
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        # log user in
        self.client.login(username="testuser", password="testpass123")
        
        # create relative objects
        self.book = Book.objects.create(name="TestBook", abbr="TB")
        self.account1 = Account.objects.create(
            name = "Test Account1",
            level3 = AccountLevel3.objects.filter(code="1101").first(),
            sub_account = "00"
        )
        self.account2 = Account.objects.create(
            name = "Test Account2",
            level3 = AccountLevel3.objects.filter(code="5101").first(),
            sub_account = "00"
        )
        self.url = reverse("transaction_create")

        self.data = {
            "book": self.book.id,
            "date": "2025-01-01",
            "description": "Test Transaction",
            # Transaction form data
            "entries-TOTAL_FORMS": "2",
            "entries-INITIAL_FORMS": "0",
            "entries-MIN_NUM_FORMS": "0",
            "entries-MAX_NUM_FORMS": "1000",
            # Entry 1
            "entries-0-account": self.account1.id,
            "entries-0-entry_type": 1,  # Dr
            "entries-0-amount": "100.00",
            # Entry 2
            "entries-1-account": self.account2.id,
            "entries-1-entry_type": 2,  # Cr
            "entries-1-amount": "100.00",

        }
        
    def test_valid_transaction_creation(self):
        """Test creating valid transaction and entries"""
        data1 = self.data.copy()
        data1["description"] = "Valid Transaction"
        response = self.client.post(self.url, data1)
        self.assertEqual(response.status_code, 302) # Redirect Succesfully
        # self.assertNotContains(response, 'alert')
        
        transaction = Transaction.objects.get(description="Valid Transaction")
        self.assertEqual(transaction.recorder, self.user)
        self.assertEqual(transaction.entries.count(), 2)

        entry1 = Entry.objects.get(transaction=transaction, account=self.account1)
        entry2 = Entry.objects.get(transaction=transaction, account=self.account2)
        self.assertEqual(entry1.amount, 100.00)
        self.assertEqual(entry1.entry_type, 1)
        self.assertEqual(entry2.amount, 100.00)
        self.assertEqual(entry2.entry_type, 2)
    
    def test_invalid_transaction_creation(self):
        data2 = self.data.copy()
        data2["description"] = "Invalid Transaction"
        data2["entries-1-amount"] = "50.00"
        response = self.client.post(self.url, data2)
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, 'alert')

        self.assertFalse(Transaction.objects.filter(description="Invalid Transaction"))
