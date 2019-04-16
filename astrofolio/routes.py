from flask import render_template, url_for, redirect, request
from astrofolio import app, db, bcrypt
from astrofolio.forms import LoginForm, NewPostForm
from astrofolio.models import Admin, Post
from flask_login import login_user, login_required, logout_user, current_user
import time
import os
import secrets


@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)

def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/blog_pics', image_fn)
    form_image.save(image_path)

    return image_fn

@app.route('/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        t = time.time()
        date = time.strftime('%b %d %Y', time.localtime(t))
        if form.image.data:
            image_file = save_image(form.image.data)
            post = Post(title=form.title.data, date=date, content=form.content.data, image=image_file, admin=current_user)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('newpost.html', title='New Post', form=form)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', post=post)

@app.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    image_path = os.path.join(app.root_path, 'static/blog_pics', post.image)
    os.remove(image_path)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newpost.html', title='Edit Post', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')
