# Gym Management System

A web-based Gym Management System built with Flask and SQLAlchemy, allowing users to view, book, and manage gym packages, as well as providing an admin dashboard for managing packages and user bookings.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
The Gym Management System is designed to streamline gym operations by providing a user-friendly interface for members to browse and book gym packages. Admin users can manage gym packages, bookings, and have access to a dashboard for administrative tasks.

## Features
- User registration and authentication
- User profile management
- Browse and book gym packages
- View personal booking history
- Admin dashboard for managing packages and viewing all bookings
- Error handling and flash messaging for user feedback

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/gym-management-system.git
    cd gym-management-system
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

6. Open the application in your browser:
    ```
    http://127.0.0.1:5000
    ```

## Usage

### User Guide
1. **Home Page**: Browse gym packages and navigate to registration or login.
2. **Registration**: Register as a new user by providing a username and password.
3. **Login**: Log in with your username and password.
4. **Profile**: Update profile details or change your password.
5. **Book Package**: Browse available packages, select a package, and book it.
6. **Booking History**: View your booking history from your profile.
7. **Admin Dashboard** (Admin Only): Manage packages, view all bookings, and access administrative tasks.

### Admin Guide
1. **Manage Packages**: Add, edit, or delete gym packages.
2. **View All Bookings**: Access a list of all user bookings.

## Screenshots
### Home Page
![Home Page](path/to/your/homepage-screenshot.png)

### Booking Page
![Booking Page](path/to/your/bookingpage-screenshot.png)

### Admin Dashboard
![Admin Dashboard](path/to/your/admindashboard-screenshot.png)

## Technologies Used
- **Flask**: Micro web framework for Python.
- **SQLAlchemy**: ORM for database management.
- **SQLite**: Lightweight database for development and testing.
- **Flask-WTF**: Provides form handling and validation.
- **Flask-Login**: Manages user authentication.
- **HTML/CSS**: Frontend design.
  
## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature.
3. Make your changes and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
