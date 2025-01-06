from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=2, unique=True)
    guideline = models.TextField(null=True, blank=True)
    currency_sign = models.CharField(max_length=1, default="$")
    
    class Meta:
        ordering = ["abbr"]
        verbose_name = ("Book")
        verbose_name_plural = ("Books")

    @property
    def record_count(self):
        return self.transactions.all().count
    
    def __str__(self):
        return self.abbr
