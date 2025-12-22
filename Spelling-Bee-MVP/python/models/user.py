import random
import sqlite3
from datetime import datetime
import re 
import hashlib

class User :
    def __init__(self, name, email, password, grade, isTeacher = False):
        self.uid = self.generate_uid()
        self.name = self.validate_name(name)
        self.email = self.validate_email(email)
        self.password = password
        self.grade = self.validate_grade(grade)
        self.isTeacher = isTeacher
        
    def generate_uid(self):
        timestamp = datetime.now().strftime("%Y%m%D%H%M%S")
        rand_num = random.randint(1000, 9999)

        return f"{timestamp}{rand_num}"

    def validate_name(self, name):
        if not isinstance(name, str):
            raise TypeError('Invalid Name Type')
            return

        test_name = name.strip()
        
        if len(test_name) == 0:
            raise ValueError('Name length must be greater than 0')
            return
        
        nameregex = re.compile(r'^[\u3040-\u309f\u4F00-\u9FFF]+$')

        if not nameregex.search(test_name):
            raise ValueError('Name is invalid type')
            return

        print(f'valid name {test_name}')
        return test_name  

    def validate_email(self, email):
        if not isinstance(email, str):
            raise TypeError('Email is invalid type')
            return
        
        test_email = email.strip().lower()

        regex = re.compile(r'[a-zA-Z0-9\.]+@[a-zA-Z0-9\.]+\.[a-zA-Z0-9]+')

        if not regex.search(test_email):
            raise ValueError('Invalid email type')
            return
        
        print(f'valid email {test_email}')
        return test_email

    def validate_grade(self, grade):
        if not isinstance(grade, str):
            raise ValueError('Wrong input, select a dropdown option')
            return

        test_grade = int(grade.strip())

        if not 2 < test_grade < 7:
            raise ValueError('This grade does not exist')
            return
        
        print(f'Valid grade, student is in grade {test_grade}')
        return test_grade

    def save(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO users (uid, name, email, password, grade, isTeacher)
        VALUES (?, ?, ?, ?, ?, ?)
        """,(self.uid, self.name, self.email, self.password, self.grade, self.isTeacher))

        conn.commit()
        conn.close()

def generate_user(name, email, password, grade):
    new_user = User(name, email, password, grade)
    print(f"""User registered successfully!
          user id: {new_user.uid}
          user name: {new_user.name}
          user email: {new_user.email}
          user password: {new_user.password}
          user grade: {new_user.grade}
          user isTeacher: {new_user.isTeacher}""")
    return new_user

if __name__ == '__main__':
    generate_user('服部太郎', 'email@email.com', 'hello1', '6')