from flask import session, jsonify
from datetime import datetime
import random
import db

class Test_attempt :
    def __init__(self, uid, grade, chapter, package, score = 0, status = 'active'):
        self.uid = uid
        self.status = status
        self.timestamp = datetime.utcnow()
        self._last_activity = self.timestamp
        self.expires_at = None
        self.grade = grade
        self.chapter = chapter
        self.score = score
        self.word_list = package
        random.shuffle(self.word_list)
        self.current_word = None
        self.attempt_id = None

    @classmethod 
    def load_attempt(cls, attempt_id):
        pass

    @property
    def last_activity(self):
        return self._last_activity
    @last_activity.setter
    def last_activity(self, value = None):
        self._last_activity = value or datetime.utcnow()

    def start_test(self):
        attempt_id = db.add_attempt(session['db_path'], (self.uid, self.timestamp, self.last_activity, self.grade, self.chapter, self.score, self.status))
        
        if attempt_id:
            self.attempt_id = attempt_id
            return True
        else:
            return False

    def timeout(self):
        self.expires_at = self.last_activity + 20 * 60
        if self.expires_at < datetime.utcnow():
            self.status = 'expired'

        db.close_attempt(session['db_path'], (self.score, self.status))

        
    def next_word(self):

        if len(self.word_list) > 0:
            self.current_word = self.word_list.pop()
            return self.current_word['japanese']
        else:
            self.current_word = None
            self.status = 'complete'
            db.close_attempt(session['db_path'], (self.score, self.status, self.attempt_id))
            return 'Test Complete!'

    
    def validate_answer(self, input):
        if self.current_word['english'] == input:
            self.score += 1
            self.last_activity()
            db.update_content(session['db_path'], (self.attempt_id, self.current_word['japanese'], self.current_word['english'], input, 1))
            return True
        else:
            self.last_activity()
            db.update_content(session['db_path'] (self.attempt_id, self.current_word['japanese'], self.current_word['english'], input, 0))
            return False, self.current_word['english']


if __name__ == '__main__':
    words = [{'japanese': '青', 'english': 'blue'},{'japanese': '赤', 'english': 'red'}, {'japanese': '黄', 'english': 'yellow'}]
    attempt = Test_attempt(3, 1, words)
    print(attempt.word_list)
    print(attempt.next_word())
    print(attempt.validate_answer('blue'))
    
