from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Book

@receiver(post_migrate)
def populate_Book(sender, **kwargs):
    MyBook = [
        ("TA","Thai Account",""),
        ("JA","Japanese Account",""),
    ]
    for (a,n) in MyBook:
        Book.objects.get_or_create(abbr=a,name=n,guideline=g)