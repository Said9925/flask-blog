from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from core import app, db
from core.models import User, Post

    

@app.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("index.html", posts=posts)


@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get(id)
    return render_template("post.html", post=post)


@app.route('/post_delete/<int:id>')
def post_delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        username = current_user.username
        posts = current_user.posts
        post_name = Post.query.filter_by(author_id=current_user.id).all()
        return render_template('profile.html', username = username, len_posts=len(posts),  post_name=post_name)
    else:
        return redirect(url_for('index'))



@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if current_user.is_authenticated:
        if request.method == 'POST':
            title = request.form.get('title')
            body = request.form.get('body')
            post = Post(title=title, body=body, author_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('new_post.html')
    else:
        return redirect(url_for('index'))
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Данные не верны')
        
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Такой пользователь уже существует!', 'danger')
            return redirect(url_for('registration'))
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/info_user/<int:id>')
def info_user(id):
    user = User.query.get(id)
    post_name = Post.query.filter_by(author_id=id).all()
    posts = user.posts
    return render_template('info_user.html', user=user, post_name=post_name, len_posts=len(posts))
