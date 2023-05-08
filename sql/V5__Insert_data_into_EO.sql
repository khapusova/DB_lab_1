INSERT INTO educational_organisations (eo_name, eo_type, location_id)
SELECT DISTINCT eoName, eoTypeName, locations.location_id
FROM zno_records
JOIN locations ON zno_records.Regname = locations.regname 
	AND zno_records.AreaName = locations.areaname 
	AND zno_records.TerName = locations.tername 
	AND zno_records.TerTypeName = locations.tertypename

