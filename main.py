import argparse
import sys

from spider_search import SpiderSearch

# добавляем вложенность рекурсии
sys.setrecursionlimit(100000)

# инициализация
parser = argparse.ArgumentParser(description="Spider search")
parser.add_argument('--url', action="store", default="http://lordsfilms.tv",
                    help="Для примера https://krasnoyarsk.pizzapertsy.ru")
parser.add_argument('--exclude', action="store", default="\.jpg|\.png|\.docx|\.docx|\.pdf|\.pdf|\.gif",
                    help="\.jpg|\.png")
parser.add_argument('--output', action="store", default="files/sitemap.xml")

# получаем параметры
args = parser.parse_args()
url = args.url.rstrip("/")

# Запускаем шарманку
search = SpiderSearch(url, exclude=args.exclude)
links = search.start()

with open(args.output, "w") as file:
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n\t<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for link in links:
        file.write("\n\t\t<url>\n\t\t\t<loc>\n\t\t\t\t{0}\n\t\t\t</loc>\n\t\t</url>".format(link))

    file.write('</urlset>')
file.close()
