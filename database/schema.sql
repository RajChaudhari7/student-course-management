DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS admins;

-- Create admins table
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create students table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    department VARCHAR(100),
    semester INT,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create courses table
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    credits INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create enrollments table
CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,

    UNIQUE(student_id, course_id)
);

-- Insert Admin
INSERT INTO admins (full_name, email, password)
VALUES
('Administrator', 'admin@gmail.com', '$2b$12$pdaPkM3.E.H6Cb607XFa8.sRBm9swd//CuS8A6BbdWaMcxZv9Fh1u');

-- Insert Students
INSERT INTO students (full_name, email, phone, department, semester, password)
VALUES
('Raj Chaudhari', 'raj@gmail.com', '9876543210', 'Computer Science', 5, '$2b$12$Yvpm/7534wrZZRymVAeoAOVrqhBCW9QHCGJ0x1GBbLVeZXy3f4bZu'),
('Aksha Vahora', 'aksha@gmail.com', '8758834505', 'Robotics', 3, '$2b$12$4Db0j1VA.L2i.llh3RpDbey6iMda4rhQKA9JDUlLNxDST5l5ZdhTO');

-- Insert Courses
INSERT INTO courses (course_name, course_code, credits)
VALUES
('Python Programming', 'PY101', 4),
('Database Management', 'DB201', 3),
('Web Development', 'WD301', 4);

-- Insert Enrollments
INSERT INTO enrollments (student_id, course_id)
VALUES
(1, 1),
(1, 2),
(2, 3);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status ENUM('Present','Absent') NOT NULL,

    FOREIGN KEY(student_id)
    REFERENCES students(id)
    ON DELETE CASCADE
);

CREATE TABLE marks (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,

    course_id INT NOT NULL,

    marks INT NOT NULL,

    grade VARCHAR(2) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,

    FOREIGN KEY(course_id)
        REFERENCES courses(id)
        ON DELETE CASCADE
);