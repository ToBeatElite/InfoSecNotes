# ToBeatElite

from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from lxml.etree import XML

# Initial Setup

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Book Model

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'desc': self.desc
        }
    
    def add_book(_title, _author, _desc):
        new_book = Book(title=_title, author=_author, desc=_desc)
        db.session.add(new_book)  
        db.session.commit() 
    
    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]

    def get_book(_id):
        return [Book.json(Book.query.filter_by(id=_id).first())]

    def update_book(_id, _title, _author, _desc):
        book_to_update = Book.query.filter_by(id=_id).first()
        book_to_update.title = _title
        book_to_update.author = _author
        book_to_update.desc = _desc
        db.session.commit()
    
    def delete_book(_id):
        Book.query.filter_by(id=_id).delete()
        db.session.commit()

db.create_all()

# API Routes

@app.route('/api/books/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def books_api(id):
    if request.method == 'GET':
        return_value = Book.get_book(id)
        return jsonify(return_value)

    elif request.method == 'PUT':
        request_data = request.get_json()
        Book.update_book(
            id,
            request_data['title'],
            request_data['author'],
            request_data['desc']
        )

        response = Response('Book Updated', status=200, mimetype='application/json')
        return response

    elif request.method == 'DELETE':
        Book.delete_book(id)
        response = Response('Book Deleted', status=200, mimetype='application/json')
        return response

@app.route('/api/add_book/', methods=['POST'])
def add_book():
    if (request.content_type.startswith('application/json')):
        request_data = request.get_json()

        Book.add_book(
            request_data['title'],
            request_data['author'],
            request_data['desc']
        )

    elif (request.content_type.startswith('application/xml')):
        request_data = request.get_data()
        content_xml = XML(request_data)
    
        Book.add_book(
            content_xml.find('title').text.strip(),
            content_xml.find('author').text.strip(),
            content_xml.find('desc').text.strip()
        )

    response = Response('Book Added', 201, mimetype='application/json')
    return response

@app.route('/api/books/', methods=['GET'])
def get_books():
    return jsonify({'Books': Book.get_all_books()})

if __name__ == '__main__':
    app.run('0.0.0.0')
