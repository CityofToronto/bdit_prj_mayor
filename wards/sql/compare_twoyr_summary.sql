DROP TABLE IF EXISTS tmp_compare;
CREATE TEMPORARY TABLE tmp_compare
(
	tmc character varying(9),
	period character varying(12),
	length_km numeric(10,4),
	ff_kph numeric(6,3),
	road_type character(3),
	tti_2014_q2 numeric(10,4),
	tti_2016_q2 numeric(10,4)
);

INSERT INTO tmp_compare
SELECT 	CTY.tmc,
	CTY.period,
	ITT.sum_miles*1.609344 AS length_km, 
	ITT.speed_new*1.609344 as ff_kph,
	CASE WHEN ITT.road_type IS NULL THEN 'LOC' ELSE ITT.road_type END AS road_type,
	CTY.tti_2014_q2,
	CTY.tti_2016_q2
	
FROM analysis.compare_twoyr CTY 
INNER JOIN gis.inrix_tmc_tor ITT USING (tmc);

DROP TABLE IF EXISTS tmp_compare2;
CREATE TEMPORARY TABLE tmp_compare2
(
	tmc character varying(9),
	period character varying(12),
	length_km numeric(10,4),
	road_type character(3),
	kph_change numeric(10,4)
);

INSERT INTO tmp_compare2
SELECT	tmc,
	period,
	length_km,
	road_type,
	(ff_kph / tti_2016_q2) - (ff_kph / tti_2014_q2) AS kph_change

FROM tmp_compare TCO
WHERE tti_2016_q2 >0 AND tti_2014_q2 > 0;

DROP TABLE IF EXISTS analysis.compare_twoyr_summary;
CREATE TABLE analysis.compare_twoyr_summary
(
	period character varying(12),
	road_type character(3),
	kph_bin smallint,
	total_km numeric(10,4)
);

INSERT INTO analysis.compare_twoyr_summary
SELECT
	period,
	road_type,
	floor(kph_change) AS kph_bin,
	SUM(length_km) AS total_km
FROM tmp_compare2 TCO2
GROUP BY period, road_type, floor(kph_change)
ORDER BY period, road_type, floor(kph_change);