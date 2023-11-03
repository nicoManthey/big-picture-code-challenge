#
# Flask application to access database
#


from time import sleep
from flask import Flask, g, session
from flask import (render_template, Response, make_response, request, redirect, jsonify)
from waitress import serve
import psycopg2.sql
import psycopg2.pool
import toml
import requests


app = Flask(__name__)


def get_db_conn():
    if 'db' not in g:
        g.db = app.config['psql_pool'].getconn()
    return g.db


def close_db_conn():
    db = g.pop('db', None)
    if db is not None:
        app.config['psql_pool'].putconn(db)
    return True


# Set routes
@app.route('/')
def index():
    """ Website index page. Show all books in the database. Needs to be 
    refreshed to show new books. """
    # Get a database connection
    db = get_db_conn()

    # Get all books from the database
    cursor = db.cursor()
    cursor.execute("SELECT isbn, author, title, summary, cover_url, bookid FROM Books.Spine")
    books = [Book(*row) for row in cursor.fetchall()]

    # Close the database connection
    close_db_conn()

    # Render the index template with the books
    return render_template('index.html', books=books)




@app.route('/books', methods=['POST'])
def save_book():
    """ Get the ISBN from the request body, validate it, fetch the book details from Open Library,
    and save the book details to the database. """
    # Get the ISBN from the request body
    isbn = request.json.get('isbn')

    # Validate the ISBN
    if not is_valid_isbn(isbn):
        return jsonify({"error": "Invalid ISBN format"}), 400

    # Fetch the book details
    open_library_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
    response = requests.get(open_library_url)
    if response.status_code != 200 or f"ISBN:{isbn}" not in response.json():
        return jsonify({"error": "ISBN not found in Open Library"}), 404
    book_data = response.json()[f"ISBN:{isbn}"]

    # Save the book details to the database
    book = Book(isbn=isbn, 
                author=book_data['authors'][0]['name'], 
                title=book_data['title'], 
                summary=book_data['excerpts'][0]['text'] if 'excerpts' in book_data else '', 
                cover_url=book_data['cover']['medium']
                )

    # Save book to DB
    db = get_db_conn()
    query = """
    INSERT INTO Books.Spine (isbn, author, title, summary, cover_url)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor = db.cursor()
    cursor.execute(query, (isbn, book.author, book.title, book.summary, book.cover_url))
    db.commit()
    close_db_conn()

    return jsonify({"message": "Book saved successfully"}), 200


@app.route('/isbn/<isbn>', methods=['GET'])
def validate_isbn(isbn):  
    
    # Validate ISBN format
    if not is_valid_isbn(isbn):
        return jsonify({"error": "Invalid ISBN format"}), 400
    
    # Make a request to the Open Library API to get book information
    open_library_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
    response = requests.get(open_library_url)
    
    if response.status_code == 200:
        # Successfully retrieved book information
        book_data = response.json()
        if f"ISBN:{isbn}" in book_data:
            return jsonify({"valid": True, "book_info": book_data[f"ISBN:{isbn}"]})
        else:
            return jsonify({"valid": False, "error": "ISBN not found in Open Library"}), 404
    else:
        return jsonify({"valid": False, "error": "ISBN not found in Open Library"}), 404


def is_valid_isbn(isbn):
    # Check if the ISBN has a valid format (10 or 13 digits)
    return isbn.isdigit() and (len(isbn) == 10 or len(isbn) == 13)


class Book:
    " Store data about a book "
    def __init__(self, isbn, author, title, summary, cover_url, bookid=None):
        self.isbn = isbn
        self.author = author
        self.title = title
        self.summary = summary
        self.cover_url = cover_url
        self.bookid = bookid


def setup_database(config: dict):
    """ 
    Connect to database and check if the schema books exists. If not, run setup_db.sql 
    to create schema books, tables and web_user. 

    Args:
        config (dict): Login credentials for database
    """
    while True:
        try:
            with psycopg2.connect(
                dbname=config['name'],
                user=config['user'],
                password=config['password'],
                host=config['host'],
                port=config['port']
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'books';")
                    schema_exists = bool(cur.rowcount)
                    print(f"Schema 'books' exists: {schema_exists}")

                    if not schema_exists:
                        with open('/db_access/setup_db.sql', 'r') as f:
                            setup_db_sql = f.read()
                        cur.execute(psycopg2.sql.SQL(setup_db_sql))
                        conn.commit()
                        print("Executed setup_db.sql")

                    print("Database setup complete")
                    break

        except psycopg2.Error as e:
            print(f"Database Error: {e}")
            sleep(2)
            continue



if __name__ == "__main__":
    app.secret_key = 'SuperSecretCookiePassword'

    # Read login credentials from file
    conn_file = '/db_access/conf.toml'
    with open(conn_file) as fin:
        f = fin.read()
    cd = toml.loads(f)
    
    # Setup database
    setup_database(cd['pgdb_setup'])
    
    app.config['psql_pool'] = psycopg2.pool.SimpleConnectionPool(
        1,10,
        user=cd['pgdb_wu']['user'],
        password=cd['pgdb_wu']['password'],
        host=cd['pgdb_wu']['host'],
        port=cd['pgdb_wu']['port'],
        database=cd['pgdb_wu']['name']
    )
    serve(app,listen='*:8000',threads=16)



