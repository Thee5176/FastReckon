from django.contrib.auth import get_user_model
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
        customuser_instance = get_user_model().objects.get(id=1)
        
        Book.objects.get_or_create(
            abbr=a,
            name=n,
            guideline=g,
            created_by=customuser_instance
        )