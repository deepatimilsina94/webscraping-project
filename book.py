import requests
from bs4 import BeautifulSoup
import sqlite3

url = 'http://books.toscrape.com/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

books = soup.find_all('article', class_='product_pod')

conn = sqlite3.connect('books.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price TEXT,
        rating TEXT
    )
''')

for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text.strip()
    rating = book.p['class'][1]  # The second class is the rating

    c.execute('INSERT INTO books (title, price, rating) VALUES (?, ?, ?)', (title, price, rating))

conn.commit()
conn.close()

print("Scraping completed and data inserted into the database.")
