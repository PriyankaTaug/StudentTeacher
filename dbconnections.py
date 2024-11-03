import psycopg2

# Define connection parameters
class DatabaseSetup:
    def __init__(self):
        self.host = "localhost"
        self.port = "5432"
        self.database = "Employeedb"
        self.user = "postgres"
        self.password = "123"
        self.conn = psycopg2.connect(
            host=self.host,       
            port=self.port,            
            database=self.database,
            user=self.user,
            password=self.password
        )

    def create_table(self):
                # Create a cursor to perform database operations
        cur = self.conn.cursor()

        # Example: Create a student_management table
        cur.execute(""" 
            CREATE TABLE IF NOT EXISTS student_management (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(50),
                classname VARCHAR(50),
                password VARCHAR(100)  
            );
        """)

        # Example: Create a teacher_management table
        cur.execute(""" 
            CREATE TABLE IF NOT EXISTS teacher_management (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(50),
                subject VARCHAR(100),
                password VARCHAR(100)  
            );
        """)


        # Create teacher_student junction table for many-to-many relationship
        cur.execute(""" 
            CREATE TABLE IF NOT EXISTS teacher_student (
                teacher_id INT REFERENCES teacher_management(id) ON DELETE CASCADE,
                student_id INT REFERENCES student_management(id) ON DELETE CASCADE,
                PRIMARY KEY (teacher_id, student_id) 
            );
        """)


         # Create teacher_student junction table for many-to-many relationship
        cur.execute("""
            CREATE TABLE IF NOT EXISTS login_log (
                id SERIAL PRIMARY KEY,
                user_type VARCHAR(10),  -- 'student' or 'teacher'
                user_id INTEGER,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                name VARCHAR(50)
            );
        """)

        # Commit the changes
        self.conn.commit()

        # Close the cursor and connection
        cur.close()
    

    def close(self):
        self.conn.close()
