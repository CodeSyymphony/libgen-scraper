from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    volume = models.CharField(max_length=255, blank=True, null=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    authors = models.CharField(max_length=255, blank=True, null=True)
    series = models.CharField(max_length=255, blank=True, null=True)
    periodical = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    edition = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255)
    pages = models.CharField(max_length=100, blank=True, null=True)
    isbn = models.CharField(max_length=255, blank=True, null=True)
    book_id = models.CharField(max_length=255, blank=True, null=True)
    time_added = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255)
    extension = models.CharField(max_length=255)
    bibtex_link = models.URLField(blank=True, null=True)
    book_image_link = models.URLField(blank=True, null=True)
    download_link = models.URLField()

    class Meta:
        verbose_name = "Latest Search Result"
        verbose_name_plural = "Latest Search Results"


class SearchQuery(models.Model):
    search_term = models.CharField(max_length=255)
    search_with_mask = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')],
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    download_link = models.URLField(max_length=200, blank=True, null=True)
    task_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Search Queries"

    def __str__(self):
        return self.search_term
