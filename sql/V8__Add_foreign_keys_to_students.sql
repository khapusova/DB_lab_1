ALTER TABLE students
ADD COLUMN location_id INT NULL;

ALTER TABLE students
ADD FOREIGN KEY (location_id) REFERENCES locations(location_id);

ALTER TABLE students
ADD COLUMN eo_id INT NULL;

ALTER TABLE students
ADD FOREIGN KEY (eo_id) REFERENCES educational_organisations(eo_id);