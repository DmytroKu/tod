import mysql.connector

config = {
    'user': 'root',
    'password': '0000',
    'host': 'localhost',
    'database': 'tod',
    'raise_on_warnings': True
}

# Встановлення з'єднання з базою даних
try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print('Підключено до бази даних MySQL')


        # Створення таблиці "students"
        create_table_query = '''
        CREATE TABLE students (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
            age INT,
           email VARCHAR(255)
        )
        '''
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print('Таблиця "students" створена')

        # Додавання студентів до таблиці "students"
        students_data = [
            ("John Doe", 20, "john.doe@example.com"),
            ("Jane Smith", 22, "jane.smith@example.com"),
            ("David Johnson", 19, "david.johnson@example.com"),
            ("Emily Brown", 21, "emily.brown@example.com"),
            ("Michael Wilson", 23, "michael.wilson@example.com")
        ]
        insert_query = "INSERT INTO students (name, age, email) VALUES (%s, %s, %s)"
        cursor.executemany(insert_query, students_data)
        connection.commit()
        print('Студенти додані до таблиці "students"')

        # Вибірка всіх студентів з таблиці "students"
        select_all_query = "SELECT * FROM students"
        cursor.execute(select_all_query)
        students = cursor.fetchall()
        print('Всі студенти з таблиці "students":')
        for student in students:
            print(student)

        # Вибірка студента за ім'ям
        select_by_name_query = "SELECT * FROM students WHERE name = %s"
        name = "John Doe"
        cursor.execute(select_by_name_query, (name,))
        student = cursor.fetchone()
        print(f'Студент з ім\'ям "{name}":')
        print(student)

        # Оновлення віку одного зі студентів
        update_age_query = "UPDATE students SET age = %s WHERE id = %s"
        new_age = 21
        student_id = 2
        cursor.execute(update_age_query, (new_age, student_id))
        connection.commit()
        print(f'Вік студента з ідентифікатором {student_id} оновлено')

        # Видалення студента за ідентифікатором
        delete_student_query = "DELETE FROM students WHERE id = %s"
        student_id = 5
        cursor.execute(delete_student_query, (student_id,))
        connection.commit()
        print(f'Студента з ідентифікатором {student_id} видалено')

        # Використання транзакцій для додавання студентів
        try:
            connection.start_transaction()

            # Дані про студентів для додавання
            additional_students_data = [
                ("Sarah Johnson", 20, "sarah.johnson@example.com"),
                ("Robert Davis", 22, "robert.davis@example.com")
            ]

            # Додавання студентів до таблиці "students"
            cursor.executemany(insert_query, additional_students_data)
            connection.commit()
            print('Додаткові студенти додані до таблиці "students"')

        except mysql.connector.Error as error:
            print('Помилка під час додавання студентів:', error)
            connection.rollback()
            print('Транзакцію скасовано')

        # Створення таблиці "courses"
        create_courses_table_query = '''
        CREATE TABLE courses (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
            description VARCHAR(255),
            credits INT
        )
        '''
        cursor.execute(create_courses_table_query)
        connection.commit()
        print('Таблиця "courses" створена')

        # Додавання курсів до таблиці "courses"
        courses_data = [
            ("Math", "Introduction to Mathematics", 3),
            ("Physics", "Introduction to Physics", 4),
            ("Chemistry", "Introduction to Chemistry", 3)
        ]
        insert_course_query = "INSERT INTO courses (name, description, credits) VALUES (%s, %s, %s)"
        cursor.executemany(insert_course_query, courses_data)
        connection.commit()
        print('Курси додані до таблиці "courses"')

        # Створення таблиці "student_courses"
        create_student_courses_table_query = '''
        CREATE TABLE student_courses (
            student_id INT,
            course_id INT,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
        '''
        cursor.execute(create_student_courses_table_query)
        connection.commit()
        print('Таблиця "student_courses" створена')

        # Дані про курси, які вибрали студенти
        student_courses_data = [
            (1, 1),  # John Doe вибрав Math
            (1, 2),  # John Doe вибрав Physics
            (2, 1),  # Jane Smith вибрала Math
            (3, 3),  # David Johnson вибрав Chemistry
            (4, 2)   # Emily Brown вибрала Physics
        ]
        insert_student_courses_query = "INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)"
        cursor.executemany(insert_student_courses_query, student_courses_data)
        connection.commit()
        print('Дані про курси студентів додані до таблиці "student_courses"')

        # Вибірка студентів, які вибрали певний курс
        select_students_by_course_query = '''
        SELECT s.*
        FROM students s
        INNER JOIN student_courses sc ON s.id = sc.student_id
        INNER JOIN courses c ON c.id = sc.course_id
        WHERE c.name = %s
        '''
        course_name = "Physics"
        cursor.execute(select_students_by_course_query, (course_name,))
        students_by_course = cursor.fetchall()
        print(f'Студенти, які вибрали курс "{course_name}":')
        for student in students_by_course:
            print(student)

        # Вибірка курсів, які вибрали студенти за певним ім'ям
        select_courses_by_student_query = '''
        SELECT c.*
        FROM courses c
        INNER JOIN student_courses sc ON c.id = sc.course_id
        INNER JOIN students s ON s.id = sc.student_id
        WHERE s.name = %s
        '''
        student_name = "John Doe"
        cursor.execute(select_courses_by_student_query, (student_name,))
        courses_by_student = cursor.fetchall()
        print(f'Курси, які вибрав студент "{student_name}":')
        for course in courses_by_student:
            print(course)

        # Вибірка студентів та їх курсів за допомогою JOIN
        select_students_and_courses_query = '''
        SELECT s.*, c.name as course_name
        FROM students s
        INNER JOIN student_courses sc ON s.id = sc.student_id
        INNER JOIN courses c ON c.id = sc.course_id
        '''
        cursor.execute(select_students_and_courses_query)
        students_and_courses = cursor.fetchall()
        print('Студенти та їх курси:')
        for row in students_and_courses:
            print(f'Student: {row[0]}, Course: {row[4]}')

except mysql.connector.Error as error:
    print('Помилка підключення до бази даних:', error)
finally:
    # Закриття з'єднання
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print('З\'єднання з базою даних закрито')
