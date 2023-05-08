CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE locations (
	location_id SERIAL PRIMARY KEY,
	regname VARCHAR(1000) NOT NULL,
	areaname VARCHAR(1000) NOT NULL,
	tername VARCHAR(1000) NOT NULL,
	tertypename VARCHAR(1000) NOT NULL
);

CREATE TABLE educational_organisations(
	eo_id SERIAL PRIMARY KEY,
	eo_name VARCHAR(1000) NOT NULL,
	eo_type VARCHAR(1000) NOT NULL,
	location_id SERIAL,
	FOREIGN KEY(location_id) REFERENCES locations(location_id)
);

CREATE TABLE students(
	student_id SERIAL PRIMARY KEY,
	outid VARCHAR(100) NOT NULL,
	birth CHAR(4) NOT NULL,
	sextypename CHAR(8) NOT NULL,
	location_id SERIAL,
	eo_id SERIAL
);

CREATE TABLE tests_results(
	tests_id SERIAL PRIMARY KEY,
	UML_test_status VARCHAR(25),
	UML_test_ball100 DECIMAL,
	UML_test_ball12 DECIMAL,
	UML_test_ball DECIMAL,
	Ukr_test_status VARCHAR(25),
	Ukr_test_ball100 DECIMAL,
	Ukr_test_ball12 DECIMAL,
	Ukr_test_ball DECIMAL,
	Hist_test_status VARCHAR(25),
	Hist_test_ball100 DECIMAL,
	Hist_test_ball12 DECIMAL,
	Hist_test_ball DECIMAL,
	Math_test_status VARCHAR(25),
	Math_test_ball100 DECIMAL,
	Math_test_ball12 DECIMAL,
	Math_test_ball DECIMAL,
	Phys_test_status VARCHAR(25),
	Phys_test_ball100 DECIMAL,
	Phys_test_ball12 DECIMAL,
	Phys_test_ball DECIMAL,
	Chem_test_status VARCHAR(25),
	Chem_test_ball100 DECIMAL,
	Chem_test_ball12 DECIMAL,
	Chem_test_ball DECIMAL,
	Bio_test_status VARCHAR(25),
	Bio_test_ball100 DECIMAL,
	Bio_test_ball12 DECIMAL,
	Bio_test_ball DECIMAL,
	Geo_test_status VARCHAR(25),
	Geo_test_ball100 DECIMAL,
	Geo_test_ball12 DECIMAL,
	Geo_test_ball DECIMAL,
	Eng_test_status VARCHAR(25),
	Eng_test_ball100 DECIMAL,
	Eng_test_ball12 DECIMAL,
	Eng_test_ball DECIMAL,
	Fr_test_status VARCHAR(25),
	Fr_test_ball100 DECIMAL,
	Fr_test_ball12 DECIMAL,
	Fr_test_ball DECIMAL,
	Deu_test_status VARCHAR(25),
	Deu_test_ball100 DECIMAL,
	Deu_test_ball12 DECIMAL,
	Deu_test_ball DECIMAL,
	Sp_test_status VARCHAR(25),
	Sp_test_ball100 DECIMAL,
	Sp_test_ball12 DECIMAL,
	Sp_test_ball DECIMAL,
	student_id SERIAL,
	FOREIGN KEY(student_id) REFERENCES students(student_id)
);



