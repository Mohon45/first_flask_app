from flask import Flask, request, jsonify
app = Flask(__name__)

book_list = [
    {
        "id": "1",
        "author": "George Orwell",
        "language": "English",
        "title": "1984"
    },
    {
        "id": "2",
        "author": "Harper Lee",
        "language": "English",
        "title": "To Kill a Mockingbird"
    },
    {
        "id": "3",
        "author": "Gabriel Garcia Marquez",
        "language": "Spanish",
        "title": "One Hundred Years of Solitude"
    },
    {
        "id": "4",
        "author": "J.K. Rowling",
        "language": "English",
        "title": "Harry Potter and the Sorcerer's Stone"
    },
    {
        "id": "5",
        "author": "Leo Tolstoy",
        "language": "Russian",
        "title": "War and Peace"
    }
]

@app.route("/")
def hello_world():
    return 'Server Running'



@app.route("/books", methods=["GET", "POST"])
def books():
    if request.method == "GET":
        if len(book_list) > 0:
            return jsonify(book_list)
        else:
            "Not Found", 404
    
    if request.method == "POST":
        printf("aise request")
        new_title = request.form["title"]
        new_author = request.form["author"]
        new_language = request.form["language"]
        iD = book_list[-1]["id"]+1

        new_book = {
            "id": iD,
            "author": new_author,
            "language": new_language
            "title": new_title
        }

        result = book_list.append(new_book)
        printf(result)
        return jsonify(result), 201

if __name__ == '__main__':
    app.run()