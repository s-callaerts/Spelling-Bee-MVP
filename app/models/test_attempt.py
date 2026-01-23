from flask import session, jsonify
import datetime
import random
import app.db as db

class Test_attempt :
    def __init__(self, uid, grade, chapter, package, score = 0, status = 'active'):
        self.uid = uid
        self.status = status
        self.timestamp = datetime.datetime.utcnow()
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
        questions, attempt_data = db.revive_attempt(attempt_id)
        
        if not questions:
            print('No unanswered questions found')
            return None
        else: 
            package = [
                {'word_id': wid,
                'japanese': jap, 
                'english': en
                }
                for (wid, jap, en) in questions]
        
        if attempt_data:
            uid, grade, chapter, score, status = attempt_data
            attempt = cls(uid, grade, chapter, package, score, status)
            attempt.attempt_id = attempt_id
            
            return attempt
        else:
            print('No attempt data')
            return False


    @property
    def last_activity(self):
        return self._last_activity
    
    @last_activity.setter
    def last_activity(self, value = None):
        self._last_activity = value or datetime.datetime.utcnow()

    def start_test(self):
        attempt_id = db.add_attempt((self.uid, self.timestamp, self.last_activity, self.grade, self.chapter, self.score, self.status))

        rows = [
            (attempt_id, word['word_id'], None, 0)
            for word in self.word_list
        ]
        
        if attempt_id:
            db.insert_content(rows)
            self.attempt_id = attempt_id
            return True
        else:
            return False

    def timeout(self):
        if self.status in ['complete', 'expired']:
            return True
        self.expires_at = self.last_activity + datetime.timedelta(minutes=20)
        if self.expires_at < datetime.datetime.utcnow():
            self.status = 'expired'
            db.close_attempt((self.last_activity, self.score, self.status, self.attempt_id))
            return True
        else:
            return False
        
    def next_word(self):
        if not self.word_list:
            self.current_word = None
            self.status = 'complete'
            db.close_attempt((self.last_activity, self.score, self.status, self.attempt_id))
            return 'Test Complete!'

        active_word = db.check_active_word(self.attempt_id)

        if active_word is not None:
            for word in self.word_list:
                if word['word_id'] == active_word:
                    self.word_list.remove(word)
                    self.current_word = word
                    return self.current_word['japanese']
        else:
            self.current_word = self.word_list.pop()
            db.set_active(self.attempt_id, self.current_word['word_id'])
            return self.current_word['japanese']

    
    def validate_answer(self, input):
        self.last_activity = datetime.datetime.utcnow()
        active_word = db.check_active_word(self.attempt_id)

        if active_word is not None:
            for word in self.word_list:
                if word['word_id'] == active_word:
                    self.word_list.remove(word)
                    self.current_word = word

        if self.current_word['english'] == input:
            self.score += 1
            db.update_content((input, 1, self.attempt_id, self.current_word['word_id']))
            db.update_test(self.attempt_id, self.last_activity, self.score)
            self.current_word = None
            return True, ''
        else:
            db.update_content((input, 0, self.attempt_id, self.current_word['word_id']))
            correct_answer = self.current_word['english']
            self.current_word = None
            return False, correct_answer
        
    def process_answer(self, user_input):
        is_correct, correct_answer = self.validate_answer(user_input)
        next_question = self.next_word()
        return is_correct, correct_answer, next_question
    
    def get_summary(self):
        total = db.get_total(self.attempt_id)

        return {
            'score': self.score,
            'total': total
        }


    
