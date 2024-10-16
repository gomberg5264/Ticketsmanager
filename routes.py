from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from models import User, Ticket
from forms import LoginForm, RegistrationForm, TicketForm
from werkzeug.security import generate_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/create_predefined_user', methods=['GET'])
def create_predefined_user():
    username = 'maxwell5264'
    password = '3YSoQH5Eq??oNpNYotT9pB&95kbY5EmMpcY8G$'
    email = 'maxwell5264@example.com'

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return 'User already exists'
    else:
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return 'Predefined user account has been created'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket()
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.status = form.status.data
        ticket.author = current_user
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket has been created!', 'success')
        return redirect(url_for('dashboard'))
    tickets = current_user.tickets.all()
    return render_template('dashboard.html', form=form, tickets=tickets)

@app.route('/ticket/<int:ticket_id>/update', methods=['GET', 'POST'])
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.author != current_user:
        flash('You do not have permission to update this ticket.', 'danger')
        return redirect(url_for('dashboard'))
    form = TicketForm()
    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.status = form.status.data
        db.session.commit()
        flash('Your ticket has been updated!', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.title.data = ticket.title
        form.description.data = ticket.description
        form.status.data = ticket.status
    return render_template('dashboard.html', form=form, update_ticket=ticket)

@app.route('/ticket/<int:ticket_id>/delete', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.author != current_user:
        flash('You do not have permission to delete this ticket.', 'danger')
        return redirect(url_for('dashboard'))
    db.session.delete(ticket)
    db.session.commit()
    flash('Your ticket has been deleted!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_all_tickets', methods=['POST'])
@login_required
def delete_all_tickets():
    current_user.tickets.delete()
    db.session.commit()
    flash('All your tickets have been deleted!', 'success')
    return redirect(url_for('dashboard'))
