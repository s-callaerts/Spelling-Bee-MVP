import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
import models.user as u
import secval.security as sec
import db

authorization_bp = Blueprint('auth', __name__, url_prefix='/auth')

@authorization_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        grade = request.form['grade']

        db.db_setup()
        error = None

        new_user = u.generate_user(name, email, password, grade)
        if new_user:
            print('User created')
        else:
            error = 'Problem creating user'

        if error is None:
            registration_success = db.add_user(new_user)
            if not registration_success:
                error = f'There was a problem registering.'
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)

    return render_template("signup.html")

@authorization_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        result = db.login_user(username)
        
        if not result:
            error = 'Error retrieving user from database'
            flash(error)
        else:
            uid, stored_password, isTeacher = result
            validation = sec.validate_login_password(password, stored_password)

            if validation:
                session.clear()
                session['uid'] = uid
                session['authority'] = isTeacher
                
                if session['authority']:
                    return redirect(url_for('teacher_dashboard'))
                else:
                    return redirect(url_for('student_dashboard'))
            else:
                error = 'Invalid password'
                flash(error)
                return render_template('login.html')