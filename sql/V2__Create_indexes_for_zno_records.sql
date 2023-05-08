CREATE INDEX idx_zno_records_outid_birth_sextypename
ON zno_records (outid, birth, sextypename);

CREATE INDEX idx_zno_records_Regname_AreaName_TerName
ON zno_records (Regname, AreaName, TerName);

CREATE INDEX idx_zno_records_EOName_EOTypeName
ON zno_records (EOName, EOTypeName);