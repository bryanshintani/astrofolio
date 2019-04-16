from astrofolio import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    posts = db.relationship('Post', backref='admin', lazy=True)

    def __repr__(self):
        return f'User: {self.id}, {self.email}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    image = db.Column(db.String())
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return f'Post: {self.id}, {self.title}, {self.date}, {self.content}, {self.image}, {self.admin_id}'
