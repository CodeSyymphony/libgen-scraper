from .models import Book
import requests
from bs4 import BeautifulSoup, NavigableString
import re
from django.db import connection
from celery import shared_task
import time


def extract_books(html_content):
    """
      Parses the given HTML content to extract book information and returns a list of books.

      Each book is represented as a dictionary with keys corresponding to book attributes such as title,
      volume, authors, series, and more. This function utilizes BeautifulSoup to navigate the HTML structure,
      specifically targeting table entries that conform to the expected layout of book information.

      Args:
          html_content (str): The HTML content fetched from a webpage containing book data.

      Returns:
          list: A list of dictionaries, where each dictionary contains details of a book.
      """
    soup = BeautifulSoup(html_content, 'html.parser')
    books = []

    for entry in soup.select('table[border="0"][rules="cols"]'):
        book = {}

        # Extracting title
        title_element = entry.select_one('td[colspan="2"] b a')
        if title_element:
            book['title'] = title_element.text.strip()
        else:
            pass

        # Extracting volume
        volume_element = entry.find('td', string=lambda x: x and 'Volume:' in x)
        if volume_element:
            book['volume'] = volume_element.find_next_sibling('td').text.strip() if volume_element.find_next_sibling(
                'td') else ''
        else:
            pass

        # Extracting topic
        topic_element = entry.find('td', string=lambda x: x and 'Topic:' in x)
        if topic_element:
            book['topic'] = topic_element.find_next_sibling('td').text.strip() if topic_element.find_next_sibling(
                'td') else ''
        else:
            pass

        # Extracting authors
        authors_element = entry.find('td', string=lambda x: x and 'Author(s):' in x)
        if authors_element:
            authors_links = authors_element.find_next_sibling('td').find_all('a')
            authors = [author_link.text.strip() for author_link in authors_links]
            book['author(s)'] = ', '.join(authors)
        else:
            book['author(s)'] = ''

        # Extracting series
        series_element = entry.find('td', string=lambda x: x and 'Series:' in x)
        if series_element:
            book['series'] = series_element.find_next_sibling('td').text.strip() if series_element.find_next_sibling(
                'td') else ''
        else:
            pass

        # Extracting periodical
        periodical_element = entry.find('td', string=lambda x: x and 'Periodical:' in x)
        if periodical_element:
            book['periodical'] = periodical_element.find_next_sibling(
                'td').text.strip() if periodical_element.find_next_sibling('td') else ''
        else:
            pass

        # Extracting publisher
        publisher_element = entry.find('td', string=lambda x: x and 'Publisher:' in x)
        if publisher_element:
            book['publisher'] = publisher_element.find_next_sibling(
                'td').text.strip() if publisher_element.find_next_sibling('td') else ''
        else:
            pass

        # Extracting city
        city_element = entry.find('td', string=lambda x: x and 'City:' in x)
        if city_element:
            book['city'] = city_element.find_next_sibling('td').text.strip() if city_element.find_next_sibling(
                'td') else ''
        else:
            pass

        # Extracting year
        year_element = entry.find('td', string=lambda x: x and 'Year:' in x)
        if year_element:
            book['year'] = year_element.find_next_sibling('td').text.strip() if year_element.find_next_sibling(
                'td') else ''
        else:
            pass

        # Extracting edition
        edition_element = entry.find('td', string=lambda x: x and 'Edition:' in x)
        if edition_element:
            book['edition'] = edition_element.find_next_sibling('td').text.strip() if edition_element.find_next_sibling(
                'td') else ''
        else:
            pass

        # Extracting language
        language_element = entry.find('td', string=lambda x: x and 'Language:' in x)
        if language_element:
            book['language'] = language_element.find_next_sibling(
                'td').text.strip() if language_element.find_next_sibling('td') else ''
        else:
            pass

        # Extracting pages quantity for books:
        pages_element = entry.find('td', string=lambda x: x and 'Pages:' in x)
        if pages_element:
            pages_data = pages_element.find_next_sibling('td')
            if pages_data:
                pages_text_parts = []
                for child in pages_data.children:
                    if isinstance(child, NavigableString):
                        pages_text_parts.append(child.strip())
                    elif child.name == 'br':
                        pages_text_parts.append('|br|')
                pages_text = ''.join(pages_text_parts)
                pages_text = pages_text.replace('|br|', ' [') + ']' if '|br|' in pages_text else pages_text
                match = re.search(r'(\d+)\s*\[\s*(\d+)\s*\]', pages_text)
                if match:
                    book['pages'] = f"{match.group(1)} [{match.group(2)}]"
                else:
                    pages_numbers = re.findall(r'\d+', pages_text)
                    book['pages'] = ', '.join(pages_numbers) if pages_numbers else ''
        else:
            book['pages'] = ''

        # Extracting ISBN
        isbn_element = entry.find('td', string=lambda x: x and 'ISBN:' in x)
        if isbn_element:
            book['isbn'] = isbn_element.find_next_sibling('td').text.strip() if isbn_element.find_next_sibling(
                'td') else ''
        else:
            pass

        # Extracing ID
        id_element = entry.find('td', string=lambda x: x and 'ID:' in x)
        if id_element:
            book['id'] = id_element.find_next_sibling('td').text.strip() if id_element.find_next_sibling('td') else ''
        else:
            pass

        # Extracting time added
        time_added_element = entry.find('td', string=lambda x: x and 'Time added:' in x)
        if time_added_element:
            book['time_added'] = time_added_element.find_next_sibling(
                'td').text.strip() if time_added_element.find_next_sibling('td') else ''
        else:
            pass

        # Extracting size
        size_element = entry.find('td', string=lambda x: x and 'Size:' in x)
        if size_element:
            size_text = size_element.find_next_sibling('td').text.strip() if size_element.find_next_sibling(
                'td') else ''
            if '(' in size_text and ')' in size_text:
                size_parts = size_text.split(' ')
                book['size'] = f"{size_parts[0]} {size_parts[1]} ({size_parts[2].strip('()')} B)"
            else:
                book['size'] = f"{size_text} B"
        else:
            pass

        # Extracting extension
        extension_element = entry.find('td', string=lambda x: x and 'Extension:' in x)
        if extension_element:
            book['extension'] = extension_element.find_next_sibling(
                'td').text.strip() if extension_element.find_next_sibling('td') else ''
        else:
            pass

        # Handling links for BibTeX, image of book and downloading book
        bibtex_link = entry.find('a', href=lambda href: href and "bibtex.php" in href)
        if bibtex_link:
            book['bib_tex'] = 'https://libgen.is' + bibtex_link['href']

        image_link = entry.find('img', src=True)
        if image_link:
            book['book_image_link'] = 'https://libgen.is' + image_link['src']

        download_link = entry.find('a', href=lambda href: href and "/get?" in href)
        if download_link:
            book['download_link'] = 'https://libgen.is' + download_link['href']

        if book and book.get('id'):
            books.append(book)
            book_instance = Book(
                title=book.get('title'),
                volume=book.get('volume', ''),
                topic=book.get('topic', ''),
                authors=book.get('author(s)'),
                series=book.get('series', ''),
                periodical=book.get('periodical', ''),
                publisher=book.get('publisher', ''),
                city=book.get('city', ''),
                year=book.get('year', ''),
                edition=book.get('edition', ''),
                language=book.get('language', ''),
                pages=book.get('pages', ''),
                isbn=book.get('isbn', ''),
                book_id=book.get('id', ''),
                time_added=book.get("time_added"),
                size=book.get('size', ''),
                extension=book.get('extension', ''),
                bibtex_link=book.get('bib_tex', ''),
                book_image_link=book.get('book_image_link', ''),
                download_link=book.get('download_link', '')
            )
            book_instance.save()
        else:
            pass

    return books


def reset_auto_increment():
    """
        Resets the auto-increment counter for the scraper_book table.

        This function clears all entries in the scraper_book table and resets the
        auto-increment ID counter to 0. It ensures that new entries start with an ID of 1.
        This is particularly useful to maintain consistency in the database after clearing
        or re-seeding data.

        Uses a database cursor to execute SQL commands directly.
    """
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM scraper_book;")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='scraper_book';")


@shared_task
def run_scraper(search_term, search_with_mask):
    """
        Initiates the scraping process with a given search term and mask option.

        This function triggers the web scraping operation on the Library Genesis
        website, fetching book details based on the provided search term. It supports
        the use of a search mask to refine search results. The function deletes all
        existing records in the Book model and resets the auto-increment ID counter
        before starting the scrape to ensure fresh data is collected.

        Parameters:
        - search_term (str): The term used for searching books.
        - search_with_mask (bool): Indicates whether to search with a wildcard mask.

        The search term spaces are replaced with plus signs for URL encoding, and
        the scraper iterates over the search results pages until no more books are found,
        accumulating all book details in a list.

        Note: Calls to `Book.objects.all().delete()` and `reset_auto_increment()` clear
        existing data in the database to ensure that the scrape starts with a clean slate.
    """
    print("Running scraper with search term:", search_term)

    Book.objects.all().delete()
    reset_auto_increment()

    # Replace spaces with plus signs in the search term for URL formatting
    search_formatted = search_term.replace(' ', '+')

    # Set the phrase parameter based on the user's choice
    phrase = "0" if search_with_mask is True else "1"

    page = 1
    all_books = list()

    while True:
        url = (
            f"https://libgen.is/search.php?req={search_formatted}&open=0&res=100&view=detailed&phrase={phrase}&column"
            f"=def&page={page}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                html_content = response.text
                books = extract_books(html_content)
                if not books:
                    break
                print(url)
                print(f"Page {page}: Extracted {len(books)} book details")
                all_books.extend(books)
                page += 1
            else:
                print(f"Skipping page {page} due to non-200 status code.")
                page += 1
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            time.sleep(1)
            page += 1
    print(f"Extracted {len(all_books)} books details")
    return all_books
