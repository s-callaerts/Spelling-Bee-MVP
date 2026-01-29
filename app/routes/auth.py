import functools
from flask import (Blueprint, render_template, request, session, url_for, jsonify, redirect)
import app.models.user as u
import app.secval.security as sec
import app.db as db
import app.schemas.schema as schema
import sqlite3

authorization_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    """check session uid to prevent unauthorized access"""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if 'uid' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

def teacher_required(f):
    """check session user status for teacher-specific dashboard"""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if 'uid' not in session or not session.get('authority'):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

def check_authority(f):
    """double check of authority for teacher-specific functions"""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('authority'):
            raise schema.SecurityError('Unauthorized access')
        return f(*args, **kwargs)
    return decorated

def json_error(e, code):
    message = str(e)
    return jsonify({'status': 'error', 'message': message}), code

def json_success(status, message):
    return jsonify({'status': status, 'message': message}), 200


@authorization_bp.route('/signup', methods=['POST'])
def register():
    try:
        data = schema.RegistrationSchema.validate(request.get_json())
    except ValueError as e:
        return json_error(e, 400)

    try:
        new_user = u.generate_user(data)
    except (ValueError, TypeError, schema.SecurityError) as e:
        return json_error(e, 400)

    registration_success = db.add_user(new_user)
    if registration_success:
        return json_success('success', 'Signup successful, redirecting to login')
    else:
        return json_error('There was a problem registering the user', 409)

@authorization_bp.route('/login', methods=['POST'])
def login():
    try:
        data = schema.LoginSchema.validate(
            request.get_json()
        )
    except ValueError as e:
        return json_error(e, 400)
    
    username = data['name']
    password = data['password']

    try:
        result = db.login_user(username)
    except sqlite3.Error as e:
        return json_error(e, 500)
    
    if result == None:
        return json_error('This user is not registered', 400)
    
    uid, stored_password, isTeacher = result

    if sec.validate_login_password(password, stored_password):
        session.clear()
        session['uid'] = uid
        session['authority'] = isTeacher
        message = 'login successful'

        if session['authority']:
            return json_success('teacher', message)
        else:
            return json_success('student', message)
    
    else:
        return json_error('username or password is incorrect', 409)
    
@authorization_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))