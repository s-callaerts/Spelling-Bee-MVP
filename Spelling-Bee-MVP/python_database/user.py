class user (self, uid, name, email, password, grade, isTeacher = False):
    def __init__(self):
        self.uid = generate_uid()
        self.name = name
        self.email = email
        self.password = hash_the_password()
        self.grade = grade
        
    def generate_uid():