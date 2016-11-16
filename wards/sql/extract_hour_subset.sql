INSERT INTO analysis.agg_extract_hour_alldata

SELECT	AEH.tmc,
	AEH.time_15_continuous,
	AEH.dt,
	AEH.count,
	AEH.avg_speed * 1.609344 AS avg_speed_kph,
	ITT.sum_miles / AEH.avg_speed * 60 AS avg_tt_min,
	NULL as pt_index
FROM inrix.agg_extract_hour_alldata AEH
INNER JOIN gis.inrix_tmc_tor ITT ON ITT.tmc = AEH.tmc
WHERE AEH.dt BETWEEN '2014-01-01' AND '2016-06-30'