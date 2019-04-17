from flask import render_template, url_for, redirect, request, current_app, Blueprint
from astrofolio import db
from astrofolio.models import Admin, Post
from astrofolio.posts.forms import NewPostForm
from astrofolio.posts.utils import save_image
from flask_login import login_required, current_user
import os
import time

posts = Blueprint('posts', __name__)

@posts.route('/new-post', methods=['GET', 'POST'])
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

        return redirect(url_for('main.home'))
    return render_template('newpost.html', title='New Post', form=form)

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', post=post)

@posts.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    image_path = os.path.join(current_app.root_path, 'static/blog_pics', post.image)
    os.remove(image_path)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('main.home'))

@posts.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newpost.html', title='Edit Post', form=form)
