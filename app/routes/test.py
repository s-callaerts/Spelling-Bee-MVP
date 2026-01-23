from flask import Blueprint, request, session, jsonify
import db
from app.routes.auth import login_required
from models import test_attempt as t

test_bp = Blueprint('main', __name__)

@test_bp.route('/test', methods=['POST'])
@login_required
def create_test():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'Error', 'message': 'Invalid JSON'}, 400)
    
    grade = data['grade']
    chapter = data['chapter']
    uid = session['uid']
    
    package = db.retrieve_words(grade, chapter)

    attempt = t.Test_attempt(uid, grade, chapter, package)
    if attempt.start_test():
        session['attempt_id'] = attempt.attempt_id
        first_word = attempt.next_word()
        return jsonify({'status': 'True', 'message': first_word})
    else:
        return jsonify({'status': 'Error', 'message': 'Error starting test'}, 500)
    
@test_bp.route('/answer', methods=['POST'])
@login_required
def submit_answer():
    #get user input from front
    try:
        data = request.get_json()

    except ValueError as e:
        return f'Error: {e}'
    
    userInput = data['answer']
    #rebuild the instance from the db
    attempt = t.Test_attempt.load_attempt(session.get('attempt_id'))
    if not attempt:
        return jsonify({'status': 'Error', 'message': 'No active attempt'}, 400)
    elif attempt.timeout():
        #upon false, front end redirects to dash
        session['attempt_id'] = None
        return jsonify({'status': 'False', 'message': 'Test timed out, returning to dashboard'})

    #check if answer is correct and get the next word    
    result = attempt.process_answer(userInput)

    if result:
        is_correct, correct_answer, next_question = result

        if next_question == 'Test Complete!':
            summary = attempt.get_summary()
            session['attempt_id'] = None
            return jsonify({
                'status': 'Complete',
                'message': next_question,
                'summary': summary
            })
        else:
            response = {
            'status': 'In Progress',
            'correct': is_correct,
            'correct_answer': correct_answer,
            'next_question': next_question
        }
        return jsonify(response)

    