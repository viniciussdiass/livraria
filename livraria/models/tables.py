from app import db
from datetime import datetime, timezone


from app import db
from datetime import datetime, timezone

class Users(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String(30), nullable=False, unique=True)
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
    data_criacao = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, nome, username, email, senha, image_file='default.jpg') -> None:
        self.nome = nome
        self.username = username
        self.email = email
        self.senha = senha
        self.image_file = image_file

    @staticmethod
    def create(nome, username, email, senha, image_file='default.jpg'):
        new_user = Users(nome, username, email, senha, image_file)
        db.session.add(new_user)
        db.session.commit()
    
    def __repr__(self):
        return f'User {self.nome}'

from livraria import db
from datetime import datetime, timezone

class Livros(db.Model):
    __tablename__ = "livros"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    overview = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(255), nullable=False, default='logo.png')
    data_cadastro = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, title, author, pages, genre, overview, image_file):
        self.title = title
        self.author = author
        self.pages = pages
        self.genre = genre
        self.overview = overview
        self.image_file = image_file
    
    @staticmethod
    def add_book(title, author, pages, genre, overview, image_file):
        new_book = Livros(title, author, pages, genre, overview, image_file)
        db.session.add(new_book)
        db.session.commit()
    
    def __repr__(self):
        return f'Livro {self.title} por {self.author}>'
