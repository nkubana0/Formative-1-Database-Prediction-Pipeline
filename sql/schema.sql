-- --------------------------
-- Loan Prediction SQL Schema
-- Author: Member A
-- --------------------------

-- Create Lookup Tables
CREATE TABLE gender (
    gender_id INT PRIMARY KEY AUTO_INCREMENT,
    gender VARCHAR(20) NOT NULL
);

CREATE TABLE education (
    education_id INT PRIMARY KEY AUTO_INCREMENT,
    level VARCHAR(50) NOT NULL
);

CREATE TABLE home_ownership (
    home_ownership_id INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(50) NOT NULL
);

CREATE TABLE loan_intent (
    intent_id INT PRIMARY KEY AUTO_INCREMENT,
    purpose VARCHAR(50) NOT NULL
);

-- Create Person Table
CREATE TABLE person (
    person_id INT PRIMARY KEY AUTO_INCREMENT,
    age INT,
    gender_id INT,
    education_id INT,
    income FLOAT,
    employment_experience INT,
    home_ownership_id INT,
    credit_score INT,
    credit_history_length INT,
    FOREIGN KEY (gender_id) REFERENCES gender(gender_id),
    FOREIGN KEY (education_id) REFERENCES education(education_id),
    FOREIGN KEY (home_ownership_id) REFERENCES home_ownership(home_ownership_id)
);

-- Create Loan Table
CREATE TABLE loan (
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    person_id INT,
    loan_amount FLOAT,
    loan_intent_id INT,
    loan_interest_rate FLOAT,
    loan_percent_income FLOAT,
    loan_status VARCHAR(50),
    previous_loan_defaults BOOLEAN,
    FOREIGN KEY (person_id) REFERENCES person(person_id),
    FOREIGN KEY (loan_intent_id) REFERENCES loan_intent(intent_id)
);

-- Insert Lookup Table Data
INSERT INTO gender (gender) VALUES ('Male'), ('Female'), ('Other');
INSERT INTO education (level) VALUES ('High School'), ('Bachelor’s'), ('Master’s');
INSERT INTO home_ownership (type) VALUES ('Own'), ('Rent'), ('Mortgage');
INSERT INTO loan_intent (purpose) VALUES ('Education'), ('Business'), ('Medical');

-- Insert Sample Person
INSERT INTO person (age, gender_id, education_id, income, employment_experience, home_ownership_id, credit_score, credit_history_length)
VALUES (30, 1, 2, 50000, 5, 1, 720, 10);

-- Insert Sample Loan
INSERT INTO loan (person_id, loan_amount, loan_intent_id, loan_interest_rate, loan_percent_income, loan_status, previous_loan_defaults)
VALUES (1, 10000, 1, 8.5, 0.2, 'Pending', FALSE);

-- Create Stored Procedure: Auto-approve high score loans
DELIMITER //

CREATE PROCEDURE auto_approve_loans()
BEGIN
    UPDATE loan
    SET loan_status = 'Approved'
    WHERE loan_status = 'Pending' AND previous_loan_defaults = FALSE AND loan_interest_rate < 10;
END //

DELIMITER ;

-- Create Log Table
CREATE TABLE loan_status_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Trigger: Log loan status changes
DELIMITER //

CREATE TRIGGER trg_log_loan_status
AFTER UPDATE ON loan
FOR EACH ROW
BEGIN
    IF OLD.loan_status <> NEW.loan_status THEN
        INSERT INTO loan_status_log (loan_id, old_status, new_status)
        VALUES (OLD.loan_id, OLD.loan_status, NEW.loan_status);
    END IF;
END //

DELIMITER ;
