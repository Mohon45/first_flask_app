from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/")
def hello_world():
    return 'Server Running'


@app.route("/books", methods=["GET", "POST"])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM book")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
    
    if request.method == "POST":
        
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form["title"]

        sql = """INSERT INTO book (author, language, title)
                VALUES (?, ?, ?)"""

        cursor = conn.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        # Fetch the last inserted book data
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM book WHERE id=?", (new_id,))
        new_book = cursor.fetchone()

        new_book_data = dict(id=new_book[0], author=new_book[1], language=new_book[2], title=new_book[3])
        
        return jsonify(new_book_data), 201


@app.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        rows = books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        for r in rows:
            book = r

        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """UPDATE book SET author=?, language=?, title=? WHERE id=?"""

        author = request.form["author"]
        language = request.form["language"]
        title = request.form["title"]

        updated_book = {
            "id": id,
            "author": author,
            "language": language,
            "title": title
        }
        print(updated_book)
        conn.execute(sql, (author, language, title, id))
        conn.commit()
        
        return jsonify(updated_book), 200
        # return "The book with id: {} has been updated.", 200

    if request.method == "DELETE":
        sql = """ DELETE FROM book WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The book with id: {} has been deleted.".format(id), 200



if __name__ == '__main__':
    app.run(debug=True)