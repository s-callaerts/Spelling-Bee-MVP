import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
import models.user as u
import secval.security as sec
import db
import static
import template

authorization_bp = Blueprint('auth', __name__, url_prefix='/auth')

@authorization_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        grade = request.form['grade']

        db = db.db_setup()
        error = None

        new_user = u.generate_user(name, email, password, grade)
        if new_user:
            print('User created')
        else:
            error = 'Problem creating user'

        if error is None:
            try:
                db.add_user(new_user)
            except db.IntegrityError:
                error = f'User {name} is already registered.'
        
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)

    return render_template("auth/register.html")

@authorization_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        try:
            uid, stored_password, isTeacher = db.login_user(username)
        except db.sqlite3.Error as e:
            error = e
            print (error)
        
        if stored_password:
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
                return render_template('login/html')