from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lisa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model for the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # New field for admin status

# Booking model to store user bookings
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_name = db.Column(db.String(150), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))

# Load user by ID for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)  # HTTP Forbidden
        return f(*args, **kwargs)
    return decorated_function

# Registration and Login Forms using Flask-WTF
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Profile Update Form
class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password (optional)')
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken. Please choose a different one.')

#package models
class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(100), nullable=False)  # e.g., "1 Month", "3 Months"


# Routes for the application
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/packages')
def packages():
    packages_list = Package.query.all()  # Retrieve all packages from the database
    return render_template('packages.html', packages=packages_list)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password, is_admin=True)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Profile Route for Viewing and Updating Profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.username.data != current_user.username:
            current_user.username = form.username.data
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    form.username.data = current_user.username
    return render_template('profile.html', form=form)

@app.route('/book_package', methods=['GET', 'POST'])
@login_required
def book_package():
    packages = Package.query.all()
    
    if request.method == 'POST':
        package_id = request.form.get('package_id')
        package = Package.query.get(package_id)
        
        new_booking = Booking(user_id=current_user.id, package_name=package.name)
        db.session.add(new_booking)
        db.session.commit()
        
        flash(f'You have successfully booked the {package.name} package!', 'success')
        return redirect(url_for('view_bookings'))
    
    return render_template('book_package.html', packages=packages)


# Route to view user's booking history
@app.route('/my_bookings')
@login_required
def view_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('my_bookings.html', bookings=bookings)

# Admin route to view all bookings
@app.route('/all_bookings')
@login_required
@admin_required
def all_bookings():
    bookings = Booking.query.all()
    return render_template('all_bookings.html', bookings=bookings)

# Admin dashboard route
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/add_package', methods=['GET', 'POST'])
@login_required
@admin_required
def add_package():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        duration = request.form.get('duration')

        # Check if a package with the same name already exists
        existing_package = Package.query.filter_by(name=name).first()
        if existing_package:
            flash('A package with that name already exists. Please choose a different name.', 'danger')
            return redirect(url_for('add_package'))

        new_package = Package(name=name, description=description, price=price, duration=duration)
        db.session.add(new_package)
        db.session.commit()

        flash('New package added successfully!', 'success')
        return redirect(url_for('manage_packages'))

    return render_template('add_package.html')



@app.route('/admin/manage_packages')
@login_required
@admin_required
def manage_packages():
    packages = Package.query.all()
    return render_template('manage_packages.html', packages=packages)

@app.route('/admin/edit_package/<int:package_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_package(package_id):
    package = Package.query.get_or_404(package_id)
    
    if request.method == 'POST':
        package.name = request.form.get('name')
        package.description = request.form.get('description')
        package.price = float(request.form.get('price'))
        package.duration = request.form.get('duration')

        db.session.commit()
        flash('Package updated successfully!', 'success')
        return redirect(url_for('manage_packages'))
    
    return render_template('edit_package.html', package=package)

@app.route('/admin/delete_package/<int:package_id>', methods=['POST'])
@login_required
@admin_required
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)
    db.session.delete(package)
    db.session.commit()
    flash('Package deleted successfully!', 'info')
    return redirect(url_for('manage_packages'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure database and tables are created
    app.run(debug=True)
