UPDATE students
SET tests_results_id = tests_results.tests_id
FROM tests_results
WHERE students.student_id = tests_results.student_id;

