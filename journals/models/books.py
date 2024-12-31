from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=2)
    record_count = models.IntegerField()
    guideline = models.TextField()
    
    class Meta:
        verbose_name = ("Book")
        verbose_name_plural = ("Books")

    def get_latest_ref(self):
        return f"{self.abbr}{self.record_count}"        

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("Book_detail", kwargs={"pk": self.pk})
