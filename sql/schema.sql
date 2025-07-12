-- --------------------------------------
-- Loan Prediction SQL Schema for SQLite
-- --------------------------------------

-- Create Lookup Tables
-- NOTE: SQLite uses INTEGER PRIMARY KEY AUTOINCREMENT
CREATE TABLE gender (
    gender_id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender VARCHAR(20) NOT NULL
);

CREATE TABLE education (
    education_id INTEGER PRIMARY KEY AUTOINCREMENT,
    level VARCHAR(50) NOT NULL
);

CREATE TABLE home_ownership (
    home_ownership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(50) NOT NULL
);

CREATE TABLE loan_intent (
    intent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    purpose VARCHAR(50) NOT NULL
);

-- Create Person Table
-- NOTE: SQLite uses REAL for floating point numbers
CREATE TABLE person (
    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    gender_id INTEGER,
    education_id INTEGER,
    income REAL,
    employment_experience INTEGER,
    home_ownership_id INTEGER,
    credit_score INTEGER,
    credit_history_length INTEGER,
    FOREIGN KEY (gender_id) REFERENCES gender(gender_id),
    FOREIGN KEY (education_id) REFERENCES education(education_id),
    FOREIGN KEY (home_ownership_id) REFERENCES home_ownership(home_ownership_id)
);

-- Create Loan Table
-- NOTE: SQLite uses INTEGER for booleans (0 for false, 1 for true)
CREATE TABLE loan (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    loan_amount REAL,
    loan_intent_id INTEGER,
    loan_interest_rate REAL,
    loan_percent_income REAL,
    loan_status VARCHAR(50),
    previous_loan_defaults INTEGER,
    FOREIGN KEY (person_id) REFERENCES person(person_id),
    FOREIGN KEY (loan_intent_id) REFERENCES loan_intent(intent_id)
);

-- Create Log Table
CREATE TABLE loan_status_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Trigger: Log loan status changes
-- NOTE: SQLite trigger syntax does not use DELIMITER
CREATE TRIGGER trg_log_loan_status
AFTER UPDATE ON loan
FOR EACH ROW
WHEN OLD.loan_status <> NEW.loan_status
BEGIN
    INSERT INTO loan_status_log (loan_id, old_status, new_status)
    VALUES (OLD.loan_id, OLD.loan_status, NEW.loan_status);
END;

-- NOTE: Stored Procedures are not supported in SQLite.
-- The logic for 'auto_approve_loans' must be handled in the Python application code.

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
VALUES (1, 10000, 1, 8.5, 0.2, 'Pending', 0);