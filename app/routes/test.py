from flask import Blueprint, request, session, jsonify
import db
from app.routes.auth import login_required
import schemas

test_bp = Blueprint('main', __name__)

test_bp.route('/test', methods=['POST'])
@login_required
def get_test_words():
    try:
        data=request.get_json()
        #make a validation schema for the values 

    except ValueError as e:
        return f'Bad package: {e}'
    
    grade = data['grade']
    chapter = data['chapter']
    
    package = db.retrieve_words(grade, chapter)
    #remember to create attempt object here and call next word

    if package:
        return jsonify(package)
    else:
        return 'Something went wrong retrieving the words'

test_bp.route('/result', methods=['POST'])
@login_required
def record_score():
    try:
        data = request.get_json()
    
    except ValueError as e:
        return 'Error:', e
    
    uid = session['uid']
    grade = data['grade']
    chapter = data['grade']
    english = [word for word in data['english']]
    user_input = [word for word in data['user_input']]
    correct = [value for value in data['correct']]
    total = data['total']

    