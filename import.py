import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))  
db = scoped_session(sessionmaker(bind=engine))

#Open CSV file
file = open("books.csv")
#Reads file
reader = csv.reader(file)

#Insert data into SQL 
for isbn, title, author, year in reader:
    db.execute("INSERT INTO cs50w_books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", 
                {"isbn": isbn, "title": title, "author": author, "year": year})

        print(f"Added book {title} to database.")

    db.commit()