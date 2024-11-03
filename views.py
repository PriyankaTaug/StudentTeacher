from dbconnections import DatabaseSetup



class  InsertStudentTeacher:
    def __init__(self):
        self.database =  DatabaseSetup()

    
    def insert_students(self,name,email,classname,password):
        try:
            with self.database.conn.cursor() as cursor:
                cursor.execute(""" INSERT INTO student_management(name,email,classname,password) values(%s,%s,%s,%s)""",(name,email,classname,password))
                self.database.conn.commit()
                print("Successfuly inserted students")
        except Exception as e:
            print(f"Error is {e}")
            self.database.conn.rollback()


    def insert_teacher(self,name,email,subject,password):
        try:
            with self.database.conn.cursor() as cursor:
                cursor.execute(""" INSERT INTO teacher_management(name,email,subject,password) values(%s,%s,%s,%s)""",(name,email,subject,password))
                self.database.conn.commit()
                print("Successfuly inserted teachers")
        except Exception as e:
            print(f"Error is {e}")
            self.database.conn.rollback()

    def view_students(self):
        try:
            with self.database.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM student_management")
                students = cursor.fetchall()  # Fetch all records
                return students  # Return the list of students
        except Exception as e:
            print(f"Error retrieving students: {e}")

    def view_teachers(self):
        try:
            with self.database.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM teacher_management")
                teachers = cursor.fetchall()  # Fetch all records
                print("teachers",teachers)
                return teachers  # Return the list of teachers
        except Exception as e:
            print(f"Error retrieving teachers: {e}")

    def add_teacher_student(self, teacher_id, student_id):
        try:
            with self.database.conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO teacher_student (teacher_id, student_id) VALUES (%s, %s)""",
                    (teacher_id, student_id)
                )
                self.database.conn.commit()
                print("Teacher-student relationship added successfully.")
        except Exception as e:
            print(f"Error adding teacher-student relationship: {e}")
            self.database.conn.rollback()


    def fetching_specific_student_teacher(self, student_id):
        with self.database.conn.cursor() as cursor:
            query = """
            SELECT t.id, t.name, t.email, t.subject
            FROM teacher_management t
            JOIN teacher_student ts ON t.id = ts.teacher_id
            WHERE ts.student_id = %s;
            """
            cursor.execute(query, (student_id,))
            data = cursor.fetchall()  # Fetch all records
            return data


    def update_student_details(self, student_id, name=None, email=None, classname=None):
        try:
            with self.database.conn.cursor() as cursor:
                update_query = "UPDATE student_management SET "
                update_fields = []
                update_values = []

                if name:
                    update_fields.append("name = %s")
                    update_values.append(name)
                if email:
                    update_fields.append("email = %s")
                    update_values.append(email)
                if classname:
                    update_fields.append("classname = %s")
                    update_values.append(classname)

                if not update_fields:
                    print("No fields to update.")
                    return

                update_query += ", ".join(update_fields) + " WHERE id = %s"
                update_values.append(student_id)  # Add student_id to the end of the values

                cursor.execute(update_query, tuple(update_values))
                self.database.conn.commit()
                print("Student information updated successfully.")
        except Exception as e:
            print(f"Error updating student: {e}")
            self.database.conn.rollback()

    def deleting_specific_student(self, student_id):
        try:
            with self.database.conn.cursor() as cursor:
                cursor.execute("DELETE FROM teacher_student WHERE student_id = %s", (student_id,))
                cursor.execute("DELETE FROM student_management WHERE id = %s", (student_id,))
                self.database.conn.commit()
                print(f"Student   successfully Deleted. {student_id}")
        except Exception as e:
            print(f"No student with this id. {student_id}")

    def login_user(self,email,password,type_data):
        with self.database.conn.cursor() as cursor:
            if type_data == 'student':
                query = """
                SELECT id, name, password
                FROM student_management
                WHERE email = %s AND password = %s;
                """
                cursor.execute(query, (email, password))
                user = cursor.fetchone()
                cursor.execute(
                    """INSERT INTO login_log(user_type, user_id,name) VALUES (%s, %s,%s)""",
                    ('student', user[0],user[1])
                )
                self.database.conn.commit()

            elif type_data == 'teacher':
                query = """
                SELECT id, name, password
                FROM teacher_management
                WHERE email = %s AND password = %s;
                """
                cursor.execute(query, (email, password))
                user = cursor.fetchone()
                cursor.execute(
                    """INSERT INTO login_log(user_type, user_id,name) VALUES (%s, %s,%s)""",
                    ('teacher', user[0],user[1])
                )
                self.database.conn.commit()
    

    def checking_userexists(self, student_id):
        with self.database.conn.cursor() as cursor:
            query = """SELECT *
                FROM student_management
                WHERE id = %s;
                """
            cursor.execute(query, (student_id,))
            data = cursor.fetchall()
            return len(data) >0


    def close_connection(self):
        self.database.conn.close()

