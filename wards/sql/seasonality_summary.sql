TRUNCATE analysis.seasonality_summary;

INSERT INTO analysis.seasonality_summary
SELECT 	SEA.year_bin, 
	SEA.month_bin,
	SEA.period,
	CASE WHEN ITT.road_type IS NULL THEN 'LOC' ELSE ITT.road_type END AS road_type, 
	SUM(ITT.sum_miles*SEA.tti_avg)/SUM(ITT.sum_miles) AS tt_ind, 
	SUM(ITT.sum_miles*(SEA.tti_95-SEA.tti_avg)/SEA.tti_avg)/SUM(ITT.sum_miles) AS buf_ind
FROM analysis.seasonality SEA
INNER JOIN gis.inrix_tmc_tor ITT USING (tmc)
GROUP BY SEA.year_bin, SEA.month_bin, SEA.period, ITT.road_type
ORDER BY CASE WHEN ITT.road_type IS NULL THEN 'LOC' ELSE ITT.road_type END, SEA.year_bin, SEA.month_bin, SEA.period;

INSERT INTO analysis.seasonality_summary
SELECT 	SEA.year_bin, 
	SEA.month_bin,
	SEA.period,
	'ALL' AS road_type, 
	SUM(ITT.sum_miles*SEA.tti_avg)/SUM(ITT.sum_miles) AS tt_ind, 
	SUM(ITT.sum_miles*(SEA.tti_95-SEA.tti_avg)/SEA.tti_avg)/SUM(ITT.sum_miles) AS buf_ind
FROM analysis.seasonality SEA
INNER JOIN gis.inrix_tmc_tor ITT USING (tmc)
GROUP BY SEA.year_bin, SEA.month_bin, SEA.period
ORDER BY SEA.year_bin, SEA.month_bin, SEA.period;