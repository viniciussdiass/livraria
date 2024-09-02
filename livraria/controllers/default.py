from livraria import app, db
from ..models.tables import Users, Livros
from flask import render_template, session, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import time


@app.route('/')
@app.route('/home')
def home():
    livros = Livros.query.order_by(Livros.id).all()
    
    return render_template('home.html', livros=livros)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('signin.html', titulo='Sign-in')

@app.route('/signup')
def signup():
    return render_template('signup.html', titulo='Sign-up')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Users.query.filter_by(username=request.form['usuario']).first()
    
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.username
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorretos!')
            return redirect(url_for('login'))
    else:
        flash('Usuário ou senha incorretos!')
        return redirect(url_for('login'))

@app.route('/cadastrar_user', methods=['POST',])
def cadastrar_user():
    nome = request.form['nome']
    username = request.form['usuario']
    email = request.form['email']
    senha = request.form['senha']
    usuario = Users.query.filter_by(username=request.form['usuario']).first()

    if usuario:
        flash('Usuario já existe!')
        return redirect(url_for('signup'))
    else:
        Users.create(nome, username, email, senha)
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('home'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_image(image_file, image_default):
    if image_file and allowed_file(image_file.filename):
        print(image_file)
        image_file_name = secure_filename(image_file.filename)
        timestamp = int(time.time())
        image_file_name = f"{image_file_name}-{timestamp}"

        image_path = os.path.join(app.config['UPLOAD_PATH'], image_file_name)

        if not os.path.exists(app.config['UPLOAD_PATH']):
            os.makedirs(app.config['UPLOAD_PATH'])

        image_file.save(image_path)
        return image_file_name
    else:
        return image_default

@app.route('/criar_livro', methods=['GET', 'POST'])
def criar_livro():
    if request.method == 'POST':
        title = request.form.get('title')
        overview = request.form.get('overview')
        author = request.form.get('author')
        pages = request.form.get('pages')
        genre = request.form.get('genre')
        image_file = request.files.get('capa')
        
        image_file_name = save_image(image_file, "logo.png")
        
        
        Livros.add_book(title=title, overview=overview, author=author, pages=pages, genre=genre, image_file=image_file_name)
        
        flash('Livro criado com sucesso!', 'success')
        return redirect(url_for('home'))
    
    return render_template('cadastrar_livro.html', titulo='Cadastrar Livro')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/livro_detail/<int:livro_id>', methods=['GET', 'POST'])
def livro_detail(livro_id):
    livro = Livros.query.get_or_404(livro_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        overview = request.form.get('overview')
        author = request.form.get('author')
        pages = request.form.get('pages')
        genre = request.form.get('genre')
        image_file = request.files.get('capa')


        livro.title = title
        livro.overview = overview
        livro.author = author
        livro.pages = pages
        livro.genre = genre
        
        if image_file and image_file.filename:
            livro.image_file = save_image(image_file, livro.image_file)
        
        db.session.commit()
        flash('Livro atualizado com sucesso!', 'success')
        return redirect(url_for('livro_detail', livro_id=livro.id))

    return render_template('livro.html', livro=livro)
