from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from datetime import datetime
from . import db, login_manager
from markdown import markdown
import bleach

class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prjID = db.Column(db.String(64))
    title = db.Column(db.String(128), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    funding = db.Column(db.String(16))
    contractor = db.Column(db.String(64), nullable=False, index=True)
    address = db.Column(db.Text, nullable=False)
    status = db.Column(db.Float, nullable=False)
    dateStart = db.Column(db.DateTime())
    dateEnd = db.Column(db.DateTime())
    agency = db.Column(db.String(64), nullable=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    region = db.Column(db.String(4))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), autoincrement=True)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    infraProj = db.relationship('Projects', backref='implementor', lazy='dynamic') 

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
	
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class scrapedProjects(db.Model):
    __tablename__ = 'dpwh'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prjID = db.Column(db.String(64))
    title = db.Column(db.Text)
    contractor = db.Column(db.String(64))
    impOffice = db.Column(db.String(64))
    srcFunds = db.Column(db.String(64))
    cost = db.Column(db.String(64))
    status = db.Column(db.String(64))
    startDate = db.Column(db.String(64))
    origComp = db.Column(db.String(64))
    actComp = db.Column(db.String(64))
    regions = db.Column(db.String(12))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    comments= db.relationship('Comment', lazy='dynamic', backref='dpwh')

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_name = db.Column(db.String(64))
    author_email = db.Column(db.String(64))
    approved = db.Column(db.Boolean, default=True)
    prjID = db.Column(db.String(64), db.ForeignKey('dpwh.prjID'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
            'h1', 'h2', 'h3', 'p'
        ]
        target.body_html = bleach.linkify(bleach.clean(
                markdown(value, output_format='html'),
                tags=allowed_tags,strip=True
            ))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)