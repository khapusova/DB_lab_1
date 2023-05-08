ALTER TABLE students
ADD COLUMN tests_results_id INT NULL;

ALTER TABLE students
ADD FOREIGN KEY (tests_results_id) REFERENCES tests_results(tests_id);