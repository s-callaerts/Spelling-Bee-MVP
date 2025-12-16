import random
import sqlite3
from datetime import datetime

class User :
    def __init__(self, uid, name, email, password, grade, isTeacher = False):
        self.uid = self.generate_uid()
        self.name = name
        self.email = email
        self.password = hash_the_password(password)
        self.grade = grade
        self.isTeacher = isTeacher
        
    def generate_uid():
        timestamp = datetime.now().strftime("%Y%m%D%H%M%S")
        rand_num = random.randint(1000, 9999)

        return f"{timestamp}{rand_num}"

    def save(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO users (uid, name, email, password, grade, isTeacher)
        VALUES (?, ?, ?, ?, ?, ?)
        """,(self.uid, self.name, self.email, self.password, self.grade, self.isTeacher))

        conn.commit()
        conn.close()