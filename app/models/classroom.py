from flask import session, jsonify
import datetime
import random
import app.database.db_classroom as db_c

class Classroom :
    def __init__(self,name, status='active', students = [], class_id = '', cr_id = ''):
        self.teacher_id = session.get(['uid'])
        self.name = name
        self.status = status
        self.students = students
        self.class_id = class_id
        self.cr_id = cr_id

    @classmethod
    def retrieve_classroom(cls):
        teacher_id = session.get(['uid'])
        data = db_c.retrieve_classroom(teacher_id)

        if data:
            name, status, class_id, students, cr_id = data
        
            classroom = cls(name, status, class_id, students, cr_id)

            return classroom
        else:
            print('No class data')
            return False
        
    def message_board():
        #set a message for students such as homework or goals
        pass
        
    def add_students():
        #add a student to the list and db
        pass

    def remove_student():
        #remove a student from the list and db
        pass

    def set_classroom_status():
        #update the classroom status
        pass

    def get_student_data():
        #retrieve students scores based on search criteria
        pass

    def calculate_average():
        #average of retrieved student scores
        pass

    def calculate_mean():
        #mean of retrieved scores
        pass
