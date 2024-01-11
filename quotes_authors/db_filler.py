import os
import json
from django import setup


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_authors.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
setup()

from authors.models import Author
from quotes.models import Quote, Tag

# with open('authors.json', 'r', encoding='utf-8') as f:
#     content = json.load(f)
#     for elem in content:
#         author = Author(fullname=elem['fullname'], born_date=elem['born_date'], born_location=elem['born_location'],
#                         description=elem['description'])
#         author.save()

with open('quotes.json', 'r', encoding='utf-8') as f:
    content = json.load(f)
    for elem in content:
        tags_names = [name for name in elem['tags']]
        try:
            author = Author.objects.get(fullname=elem['author'])
            quote = Quote(author=author, quote=elem['quote'])
            quote.save()
            tags_names = [name for name in elem['tags']]
            tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tags_names]
            quote.tags.set(tags)
        except Author.DoesNotExist:
            print("Автор не знайдений.")
            continue
