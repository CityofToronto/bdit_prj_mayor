TRUNCATE analysis.seasonality;

INSERT INTO 	analysis.seasonality
SELECT 		tmc, 
		extract(year from dt) AS year_bin, 
		extract(month from dt) AS month_bin, 
		TPE.period, avg(tt_index) AS tti_avg, 
		percentile_cont(0.5) WITHIN GROUP (ORDER BY tt_index) AS tti_med, 
		percentile_cont(0.95) WITHIN GROUP (ORDER BY tt_index) AS tti_95
		
FROM analysis.agg_extract_hour_alldata AEH
INNER JOIN ref.timeperiod TPE USING (time_15_continuous)
LEFT JOIN ref.holiday HOL USING (dt)

WHERE HOL.dt IS NULL AND EXTRACT(dow from dt) IN (1,2,3,4,5)

GROUP BY tmc, extract(year from dt), extract(month from dt), TPE.period