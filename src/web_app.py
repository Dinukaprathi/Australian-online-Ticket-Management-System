from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import StringField, PasswordField, EmailField, IntegerField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os

from src.models.database import db
from src.models.user import User
from src.models.ticket import Ticket, TicketType, TicketCategory
from src.services.ticket_service import TicketService
from src.services.user_service import UserService

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aotms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ticket_service = TicketService()
user_service = UserService()

# Create database tables
with app.app_context():
    db.create_all()

# Create static directory if it doesn't exist
os.makedirs(os.path.join(app.root_path, 'static'), exist_ok=True)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=120)])
    concession_card = StringField('Concession Card Number (Optional)')

def validate_date(form, field):
    """Validate that the date is within the tournament period"""
    try:
        selected_date = field.data
        if not isinstance(selected_date, datetime):
            selected_date = datetime.combine(selected_date, datetime.min.time())
        
        start_date = datetime(2026, 1, 18)
        end_date = datetime(2026, 2, 2, 23, 59, 59)  # End of day on Feb 2
        
        if not start_date <= selected_date <= end_date:
            raise ValueError("Date must be between Jan 18 and Feb 2, 2026")
    except Exception as e:
        raise ValueError("Invalid date format. Please select a date between Jan 18 and Feb 2, 2026")

class TicketPurchaseForm(FlaskForm):
    ticket_type = SelectField('Ticket Type', choices=[
        (TicketType.GROUND_PASS_WEEK1.value, f"{TicketType.GROUND_PASS_WEEK1.value} - Regular: $49, Concession: $25, Youth: $10, Kids: $25"),
        (TicketType.GROUND_PASS_MIDDLE.value, f"{TicketType.GROUND_PASS_MIDDLE.value} - Regular: $69, Concession: $30, Youth: $10, Kids: $30"),
        (TicketType.GROUND_PASS_WEEK2.value, f"{TicketType.GROUND_PASS_WEEK2.value} - Regular: $139, Concession: $70, Youth: $5, Kids: $70"),
        (TicketType.ROD_LAVER.value, f"{TicketType.ROD_LAVER.value} - Regular: $75, Concession: $37.50, Youth: $37.50, Kids: $37.50"),
        (TicketType.MARGARET_COURT.value, f"{TicketType.MARGARET_COURT.value} - Regular: $65, Concession: $32.50, Youth: $32.50, Kids: $32.50"),
        (TicketType.JOHN_CAIN.value, f"{TicketType.JOHN_CAIN.value} - Regular: $65, Concession: $32.50, Youth: $32.50, Kids: $32.50"),
        (TicketType.AO_LIVE.value, f"{TicketType.AO_LIVE.value} - Regular: $20, Concession: $10, Youth: $10, Kids: $10")
    ])
    category = SelectField('Category', choices=[
        (TicketCategory.ADULT.value, f"{TicketCategory.ADULT.value} (18+ years)"),
        (TicketCategory.CONCESSION.value, f"{TicketCategory.CONCESSION.value} (Seniors, Students)"),
        (TicketCategory.YOUTH.value, f"{TicketCategory.YOUTH.value} (12-17 years)"),
        (TicketCategory.KIDS.value, f"{TicketCategory.KIDS.value} (3-11 years)")
    ])
    session_date = DateField('Session Date', format='%Y-%m-%d', validators=[DataRequired(), validate_date])
    concession_card = StringField('Concession Card Number (if applicable)')
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=10)], default=1)
    submit = SubmitField('Purchase Ticket')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Check if username or email already exists
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already exists', 'danger')
                return render_template('auth/register.html', form=form)
            
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered', 'danger')
                return render_template('auth/register.html', form=form)

            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,  # Password will be hashed in User.__init__
                full_name=form.full_name.data,
                age=form.age.data,
                concession_card=form.concession_card.data or None
            )
            
            db.session.add(user)
            db.session.commit()
            
            login_user(user)
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error during registration: {str(e)}', 'danger')
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/tickets/purchase', methods=['GET', 'POST'])
@login_required
def purchase_ticket():
    form = TicketPurchaseForm()
    if form.validate_on_submit():
        try:
            ticket_type = form.ticket_type.data
            category = form.category.data
            session_date = form.session_date.data
            quantity = form.quantity.data
            concession_card = form.concession_card.data

            # Validate concession card if category is Concession
            if category == TicketCategory.CONCESSION.value and not concession_card:
                flash('Concession card number is required for concession tickets', 'danger')
                return redirect(url_for('purchase_ticket'))

            ticket = ticket_service.purchase_ticket(
                user=current_user,
                ticket_type=ticket_type,
                category=category,
                session_date=session_date,
                quantity=quantity,
                concession_card=concession_card
            )

            flash('Ticket purchased successfully!', 'success')
            return redirect(url_for('view_tickets'))

        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('purchase_ticket'))

    # Get available sessions for the next 7 days
    available_sessions = ticket_service.get_available_sessions()
    return render_template('tickets/purchase.html', 
                         form=form,
                         available_sessions=available_sessions,
                         ticket_types=TicketType,
                         categories=TicketCategory)

@app.route('/tickets')
@login_required
def view_tickets():
    tickets = current_user.tickets
    return render_template('tickets/view.html', tickets=tickets)

@app.route('/tickets/update/<int:ticket_id>', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Check if the ticket belongs to the current user
    if ticket.user_id != current_user.id:
        flash('You do not have permission to update this ticket.', 'danger')
        return redirect(url_for('view_tickets'))
    
    try:
        quantity = int(request.form.get('quantity', 1))
        concession_card = request.form.get('concession_card')
        
        if quantity < 1 or quantity > 10:
            flash('Quantity must be between 1 and 10.', 'danger')
            return redirect(url_for('view_tickets'))
        
        # Update ticket
        ticket.quantity = quantity
        ticket.concession_card = concession_card if concession_card else None
        
        db.session.commit()
        flash('Ticket updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating ticket: {str(e)}', 'danger')
    
    return redirect(url_for('view_tickets'))

@app.route('/tickets/delete/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Check if the ticket belongs to the current user
    if ticket.user_id != current_user.id:
        flash('You do not have permission to delete this ticket.', 'danger')
        return redirect(url_for('view_tickets'))
    
    try:
        db.session.delete(ticket)
        db.session.commit()
        flash('Ticket deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting ticket: {str(e)}', 'danger')
    
    return redirect(url_for('view_tickets'))

if __name__ == '__main__':
    app.run(debug=True) 