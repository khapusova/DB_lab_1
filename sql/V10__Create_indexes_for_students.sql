CREATE INDEX idx_students_location_id
ON students (location_id);

CREATE INDEX idx_students_eo_id
ON students (eo_id);

CREATE INDEX idx_students_outid_birth_sextypename
ON students (outid, birth, sextypename);