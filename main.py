import logging
from dbconnections import DatabaseSetup
from views import InsertStudentTeacher

class MainStart:

    def __init__(self):
        # Connecting to the postgres database
        self.database = DatabaseSetup()
        self.views = InsertStudentTeacher()


    def table_setuping(self):
        """Creating tables in the database named student_management and teacher_managemnet"""
        self.database.create_table()
        self.database.close()


    def insert_data(self):
        """Inserting the student data """
        name ="Ram"
        email = "ram@gmail.com"
        classname = "I"
        password = "123"
        self.views.insert_students(name,email,classname,password)

        """Inserting the teacher data"""
        name ="Priya"
        email = "priya@gmail.com"
        subject = "IMaths"
        password = "123"
        self.views.insert_teacher(name,email,subject,password)


    def view_details(self):
        """View students details """
        view_students = self.views.view_students()
        for students in view_students:
            print(students)

        """View teachers details """
        view_teachers = self.views.view_teachers()
        for teachers in view_teachers:
            print(teachers)



    def updating_student_details(self):
        """updating student details"""
        self.views.update_student_details(student_id=1,name="Suresh",email="suresh@gmail")



    def adding_relation(self):
        """adding student teacher relation"""
        self.views.add_teacher_student(1,8)


    def fetching_student_teachers(self):
        """fetching specific student teachers"""
        self.views.fetching_specific_student_teacher(6)


    def deleting_student(self):
        """deleting aspecific student"""
        studentid = 3
        if self.views.checking_userexists(studentid):
            print("hai",self.views.checking_userexists)
            self.views.deleting_specific_student(studentid)
            print("Sucessfully deleted")
        else:
            print("Student Not Exists")


    def login_data(self):
        """loging student or teacher"""
        self.views.login_user(email="priya@gmail.com", password="123", type_data="teacher")


    def close_connection(self):
        """Close the database connection"""
        self.database.close()

if __name__ == "__main__":
    app = MainStart()
    app.table_setuping()
    app.insert_data()
    app.view_details()
    app.adding_relation()
    app.fetching_student_teachers()
    app.deleting_student()
    app.login_data()
    app.close_connection()