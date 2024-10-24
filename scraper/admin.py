from django.contrib import admin
from .models import SearchQuery, Book
from .tasks import run_scraper
from django.urls import reverse
from django.utils.html import format_html


# Register your models here.


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('search_term', 'status', 'created_at', 'completed_at', 'download_link_html')
    fields = ('search_term', 'search_with_mask', 'status', 'created_at', 'completed_at', 'download_link_html')
    readonly_fields = ('status', 'created_at', 'completed_at', 'download_link_html')

    def download_link_html(self, obj):
        if obj.status == 'completed' and obj.download_link:
            return format_html("<a href='{}' download>Download</a>", obj.download_link)
        return "Not available"
    download_link_html.short_description = "Download Link"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # To avoid re-triggering on updates
            # Start the scrape task with only the ID of the object
            task = run_scraper.delay(obj.id)
            obj.task_id = task.id
            obj.save()


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'publisher', 'year', 'isbn')
    list_filter = ('authors', 'publisher', 'year')
    search_fields = ('title', 'authors', 'isbn')
