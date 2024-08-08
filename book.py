import requests
from bs4 import BeautifulSoup
import sqlite3

# Navigate to the website
url = 'http://books.toscrape.com/'

# Get the page source and create a BeautifulSoup object
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the book details
books = soup.find_all('article', class_='product_pod')

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('books.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price TEXT,
        rating TEXT
    )
''')

# Insert book details into the table
for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text.strip()
    rating = book.p['class'][1]  # The second class is the rating

    c.execute('INSERT INTO books (title, price, rating) VALUES (?, ?, ?)', (title, price, rating))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Scraping completed and data inserted into the database.")
