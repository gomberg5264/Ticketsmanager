from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    tickets = db.relationship('Ticket', backref='author', lazy='dynamic', foreign_keys='Ticket.user_id')
    assigned_tickets = db.relationship('Ticket', backref='assigned_to', lazy='dynamic', foreign_keys='Ticket.assigned_user_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='low')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    closed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Ticket {self.title}>'
