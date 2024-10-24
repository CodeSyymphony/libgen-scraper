from celery import shared_task
from .scraper import run_scraper as scraper_function
from .models import SearchQuery, Book
from .resources import BookResource
import json
from django.utils import timezone
from django.conf import settings
import zipfile
import os
import logging

logger = logging.getLogger(__name__)


def sanitize_filename(filename, search_with_mask):
    allowed_special_chars = ['_', '-']
    sanitized = "".join(c if c.isalnum() or c in allowed_special_chars else '_' for c in filename)
    if search_with_mask:
        sanitized += "_with_mask"
    return sanitized


@shared_task
def run_scraper(search_query_id):
    try:
        search_query = SearchQuery.objects.get(pk=search_query_id)
        search_term = search_query.search_term
        search_with_mask = search_query.search_with_mask

        books = scraper_function(search_term, search_with_mask)

        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        sanitized_search_term = sanitize_filename(search_term, search_with_mask)
        creation_date = timezone.now().strftime('%Y%m%d-%H%M%S')

        zip_filename = f"{sanitized_search_term}_{creation_date}.zip"
        zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

        csv_filename = f"{sanitized_search_term}_{creation_date}.csv"
        json_filename = f"{sanitized_search_term}_{creation_date}.json"
        csv_path = os.path.join(settings.MEDIA_ROOT, csv_filename)
        json_path = os.path.join(settings.MEDIA_ROOT, json_filename)

        book_resource = BookResource()
        dataset = book_resource.export()

        with open(csv_path, 'w', encoding='utf-8') as csv_file:
            csv_file.write(dataset.csv)

        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(books, json_file)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(csv_path, arcname=csv_filename)
            zipf.write(json_path, arcname=json_filename)

        # Clean up the temporary files
        os.remove(csv_path)
        os.remove(json_path)

        search_query.download_link = settings.MEDIA_URL + zip_filename
        search_query.status = 'completed'
        search_query.completed_at = timezone.now()
        search_query.save()
        logger.info(f"Scraping completed successfully: {zip_filename}")
        return {'zip_filename': zip_filename}
    except Exception as e:
        logger.error(f"Error in run_scraper task: {e}")
        search_query.status = 'failed'
        search_query.save()
        raise e
