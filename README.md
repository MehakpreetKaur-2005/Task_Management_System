# TASKMANAGEMENTSYSTEM
The Task Management System help individuals or teams organize, track, and manage their tasks effectively. The system allows users to create, update, set deadlines, and track progress.
A dynamic and secure web-based Task Management System designed to streamline and enhance the way users manage their daily tasks. Built with Flask, SQLite, and SQLAlchemy, it focuses on simplicity, usability, and robust functionality.

////FEATURES
User Registration and Secure Login
Create, Read, Update, Delete (CRUD) tasks
Mark tasks as Complete or Incomplete
Real-time task statistics (total, completed, pending)
User-specific task management and session handling
Responsive and user-friendly UI using HTML5, CSS3, Bootstrap, and Jinja2 templates
Passwords secured with hashing algorithms
Scalable and modular architecture for future expansion


//// TECHNOLOGIES USED
Frontend: HTML5, CSS3, Bootstrap, JavaScript
Backend: Python (Flask Framework)
Database: SQLite (via SQLAlchemy ORM)
Others: Flask-WTF, Werkzeug Security, Flask-SQLAlchemy


////SYSTEM DESIGN OVERVIEW
Presentation Layer: Flask templates (HTML/CSS/JS)
Application Layer: Flask App with routes, session management
Data Layer: SQLite database with relational schemas
Authentication: Secure login system with hashed passwords


////DATABASE SCHEMA
User Table: id, username, email, password (hashed), created_date
Task Table: task_id, title, description, status (completed/pending), due_date, user_id (FK)


////FUTURE ENHANCEMENTS
Add priority levels to tasks (High, Medium, Low)
Implement reminder notifications
Allow collaborative task management (team features)
Switch to production-ready databases like PostgreSQL
Add API support for mobile app integration


////REFERENCES
Flask Documentation
SQLAlchemy Documentation
W3Schools Tutorials


////AUTHORS
Mehakpreet Kaur (RA2311003020175)
Shreya Rahul Jain (RA2311003020193)
