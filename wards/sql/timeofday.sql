TRUNCATE analysis.timeofday;

INSERT INTO analysis.timeofday
SELECT tmc, extract(year from dt) AS year_bin, floor(time_15_continuous/10) AS hour_bin, avg(tt_index) AS tti_avg, percentile_cont(0.5) WITHIN GROUP (ORDER BY tt_index) AS tti_med, percentile_cont(0.95) WITHIN GROUP (ORDER BY tt_index) AS tti_95
FROM analysis.agg_extract_hour_alldata AEH
LEFT JOIN ref.holiday HOL USING (dt)
WHERE HOL.dt IS NULL AND EXTRACT(dow from dt) IN (1,2,3,4,5) AND EXTRACT(month from dt) < 7
GROUP BY tmc, extract(year from dt), floor(time_15_continuous/10);