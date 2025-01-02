from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=2, unique=True)
    record_count = models.IntegerField(null=True, blank=True)
    guideline = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ["abbr"]
        verbose_name = ("Book")
        verbose_name_plural = ("Books")

    def get_latest_ref(self):
        return f"{self.abbr}{self.record_count}"        

    def __str__(self):
        return self.abbr
