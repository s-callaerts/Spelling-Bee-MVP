import random
import sqlite3
from datetime import datetime
import re 
from app.secval import security as sec
from app.schemas.schema import SecurityError

class User :
    def __init__(self, payload, isTeacher = False):
        self.uid = self.generate_uid()
        self.name = self.validate_name(payload['name'])
        self.email = self.validate_email(payload['email'])
        self.password = sec.hash_password(self.validate_password(payload['password']))
        self.grade = self.validate_grade(payload['grade'])
        self.isTeacher = isTeacher
        
    def generate_uid(self):
        timestamp = datetime.now().strftime("%Y%m%D%H%M%S")
        rand_num = random.randint(1000, 9999)

        return f"{timestamp}{rand_num}"

    def validate_name(self, name):
        if not isinstance(name, str):
            raise TypeError('Invalid Name Type')

        test_name = name.strip()
        
        if len(test_name) == 0:
            raise ValueError('Name length must be greater than 0')
        
        nameregex = re.compile(r'^[\u3040-\u309f\u4F00-\u9FFF]+$')

        if not nameregex.search(test_name):
            raise ValueError('Name is invalid type')

        print(f'valid name {test_name}')
        return test_name  

    def validate_email(self, email):
        if not isinstance(email, str):
            raise TypeError('Email is invalid type')
        
        test_email = email.strip().lower()

        regex = re.compile(r'[a-zA-Z0-9\.]+@[a-zA-Z0-9\.]+\.[a-zA-Z0-9]+')

        if not regex.search(test_email):
            raise ValueError('Invalid email type')
        
        print(f'valid email {test_email}')
        return test_email
    
    def validate_password(self, password):
        if not isinstance(password, str):
            raise TypeError('Invalid password type')
        
        if len(password) < 8:
            raise SecurityError('パスワードは8文字以上にしてください')
        
        if not re.search(r'[.$@!#?0-9]', password):
            raise SecurityError('パスワードに番号および(.$@!#?)文字のひとつを含めてください')
        
        return password

    def validate_grade(self, grade):
        if not isinstance(grade, int):
            raise ValueError('Wrong input, select a dropdown option')

        if not 2 < grade < 9:
            raise ValueError('This grade does not exist')
        
        print(f'Valid grade, student is in grade {grade}')
        return grade

    def save(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO users (uid, name, email, password, grade, isTeacher)
        VALUES (?, ?, ?, ?, ?, ?)
        """,(self.uid, self.name, self.email, self.password, self.grade, self.isTeacher))

        conn.commit()
        conn.close()

def generate_user(payload):
    new_user = User(payload)
    print(f"""User registered successfully!
          user id: {new_user.uid}
          user name: {new_user.name}
          user email: {new_user.email}
          user password: {new_user.password}
          user grade: {new_user.grade}
          user isTeacher: {new_user.isTeacher}""")
    print(new_user)

    return(new_user.uid, new_user.name, new_user.email, new_user.password, new_user.grade, new_user.isTeacher)
