
# Big Picture Coding Challenge - Backend - Book Library API

## Nico's Comments & How to run

To run this website, run:
```
docker-compose up
```

This will create 3 containers: 
- postgreSQL database.
- pgAdmin which can be reached by typing http://localhost:8080 in the browser
- website which can be reached by typing http://localhost:7070

**Connect to pgAdmin (optional)**
Open http://localhost:8080, login with nico.manthey@gmail.com, PW: 1234. 
The database is not yet connected. On the left, right-click on servers > register > server. 
Under the tab General, type some Name, e.g. my_books_db. 
Under the tab Connection, type
- Host name/address: psqldb
- Port: 5432
- Maintenance database: books_db
- Username: postgres
- Password: 1234

Now, click Save. PgAdmin is now set up. 

**Website**
The website has 3 functionalities:
- Check a ISBN number. If it's not a correct ISBN, show an alert. If it's a correct ISBN, fetch data from openlibrary.org and display as json in browser.
- Add book to database via some input ISBN. If ISBN is invalid, show alert. If ISBN is valid, get book data from openlibarary.org, add it to database and show success message.
- Books that are stored in the database are display on the website. After a new book was added, the website needs to be refreshed in order to show the new book.

## Original Instructions

**To work on this challenge, please create a fork of it to your own github account**

Our colleagues have amassed an impressive collection of books, leading to quite the bill and an unhappy boss. To keep things organized and to provide transparency into our library, we've decided to step in and help with software. Our solution: a sleek website where our intern can easily record books by their ISBN number, pulling in detailed information via an API.

**Your mission**: Build the backend to power this application.

## Overview:

- Users (in this case, our intern) can enter the ISBN number of a book.
- Our software will fetch the book's details from an external API and save it to our database.
- The frontend will then display our entire library in a user-friendly manner.

## Backend Specifications:

### Technology:

- Python (Any backend framework of your choice. E.g., Flask, Django, FastAPI, etc.)
- ORM + Database: Feel free to choose what you're comfortable with (SQLite, PostgreSQL, MongoDB, etc.)

### Features:

1. **ISBN Validation**:
    - The backend should be able to validate an ISBN number.
    - If the ISBN is not valid, it should send an appropriate response to the frontend.

2. **Fetch Book Details**:
    - The backend should get book details like author, title, summary, and cover URL from a third-party API.
    - Hint: Check out [OpenLibrary's API](https://openlibrary.org/). It's free and provides detailed information on books by ISBN.

3. **Endpoints**:

    - **Task 1**: Fetch Book Details by ISBN

      `GET /isbn/<isbn>`:
      - Returns a JSON including: author, title, summary, cover_url.

    - **Task 2**: Save Book Details to our Library

      `POST /books` with body `JSON: {isbn: "ISBN_NUMBER_HERE"}`:
      - This will save the book's details to our library database.

    - **Task 3**: List All Books in our Library

      `GET /books`:
      - Returns a list of all books stored in our library.
      - Use a format, so the fronend can render all information from this one JSON

## Documentation:

Please ensure that you document your code adequately. Proper commenting will not only help you in future modifications but will also assist any other developer who might be working with your code.

## Installation
*Please tell us how to get your code running. Do we need to install anything? Is there a database we need to create? Please provide all necessary instructions. After following these instructions the code should run!*

Good luck, and may your code run without bugs!

