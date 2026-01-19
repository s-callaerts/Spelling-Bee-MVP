from flask import session, jsonify
from datetime import datetime
import random

class Test_attempt :
    def __init__(self, grade, chapter, package, score = 0, status = 'active'):
        #self.uid = session['uid']
        self.status = status
        self.timestamp = datetime.now().strftime("%Y%m%D%H%M%S")
        self.last_activity = datetime.now().strftime("%Y%m%D%H%M%S")
        self.expires_at = None
        self.grade = grade
        self.chapter = chapter
        self.score = score
        self.word_list = package
        random.shuffle(self.word_list)
        self.current_word = None
        
    def next_word(self):

        if len(self.word_list) > 0:
            self.current_word = self.word_list.pop()
            return self.current_word['japanese']
        else:
            self.current_word = None
            return 'Test Complete!'

    
    def validate_answer(self, input):
        if self.current_word['english'] == input:
            self.score += 1
            #setter last_activity
            #write to db here
            return True
        else:
            #setter last_activity
            #write to db
            return False, self.current_word['english']


if __name__ == '__main__':
    words = [{'japanese': '青', 'english': 'blue'},{'japanese': '赤', 'english': 'red'}, {'japanese': '黄', 'english': 'yellow'}]
    attempt = Test_attempt(3, 1, words)
    print(attempt.word_list)
    print(attempt.next_word())
    print(attempt.validate_answer('blue'))
    
