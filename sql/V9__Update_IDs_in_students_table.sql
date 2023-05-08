UPDATE students
SET location_id = loc.location_id,
    eo_id = eo.eo_id
FROM zno_records z
JOIN locations loc ON z.Regname = loc.regname
                   AND z.AreaName = loc.areaname
                   AND z.TerName = loc.tername
JOIN educational_organisations eo ON z.EOName = eo.eo_name
                                 AND z.EOTypeName = eo.eo_type
WHERE students.location_id IS NULL AND students.eo_id IS NULL
  AND students.outid = z.outid
  AND students.birth = z.birth
  AND students.sextypename = z.sextypename