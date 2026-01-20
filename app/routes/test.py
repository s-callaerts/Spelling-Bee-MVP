from flask import Blueprint, request, session, jsonify
import db
from app.routes.auth import login_required
from models import test_attempt

test_bp = Blueprint('main', __name__)

test_bp.route('/test', methods=['POST'])
@login_required
def create_test():
    try:
        data=request.get_json()
        #make a validation schema for the values 

    except ValueError as e:
        return f'Bad package: {e}'
    
    grade = data['grade']
    chapter = data['chapter']
    uid = session['uid']
    
    package = db.retrieve_words(grade, chapter)

    attempt = test_attempt.TestAttempt(uid, grade, chapter, package)
    if attempt.start_test():
        first_word = attempt.next_word()
        return jsonify({'question': first_word})
    else:
        return 'Error starting test', 500
    
test_bp.route('/answer', methods=['POST'])
@login_required
def submit_answer():
    try:
        data = request.get_json()

    except ValueError as e:
        return f'Error: {e}'
    
    userInput = data['answer']
    #result = attempt.validate_answer(userInput)
    
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

    