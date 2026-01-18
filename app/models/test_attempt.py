from flask import session, jsonify
import datetime

class Test_attempt :
    def __init__(self, grade, chapter, package, score = 0, status = 'active'):
        self.uid = session['uid']
        self.status = status
        self.timestamp = datetime.now()
        self.last_activity = datetime.now()
        self.expires_at = None
        self.grade = grade
        self.chapter = chapter
        self.score = score
        self.test_content = package