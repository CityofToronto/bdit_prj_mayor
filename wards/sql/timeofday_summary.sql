TRUNCATE analysis.timeofday_summary;

INSERT INTO analysis.timeofday_summary
SELECT 	TOD.year_bin, 
	TOD.hour_bin, 
	CASE WHEN ITT.road_type IS NULL THEN 'LOC' ELSE ITT.road_type END AS road_type, 
	SUM(ITT.sum_miles*TOD.tti_avg)/SUM(ITT.sum_miles) AS tt_ind, 
	SUM(ITT.sum_miles*(TOD.tti_95-TOD.tti_avg)/TOD.tti_avg)/SUM(ITT.sum_miles) AS buf_ind
FROM analysis.timeofday TOD
INNER JOIN gis.inrix_tmc_tor ITT USING (tmc)
GROUP BY TOD.year_bin, TOD.hour_bin, ITT.road_type
ORDER BY CASE WHEN ITT.road_type IS NULL THEN 'LOC' ELSE ITT.road_type END, TOD.year_bin, TOD.hour_bin;

INSERT INTO analysis.timeofday_summary
SELECT 	TOD.year_bin, 
	TOD.hour_bin, 
	'ALL' AS road_type, 
	SUM(ITT.sum_miles*TOD.tti_avg)/SUM(ITT.sum_miles) AS tt_ind, 
	SUM(ITT.sum_miles*(TOD.tti_95-TOD.tti_avg)/TOD.tti_avg)/SUM(ITT.sum_miles) AS buf_ind
FROM analysis.timeofday TOD
INNER JOIN gis.inrix_tmc_tor ITT USING (tmc)
GROUP BY TOD.year_bin, TOD.hour_bin
ORDER BY TOD.year_bin, TOD.hour_bin;