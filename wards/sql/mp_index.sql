TRUNCATE analysis.mp_index;

INSERT INTO analysis.mp_index

SELECT 	tmc, 
	EXTRACT(YEAR from AEH.dt) as year_bin, 
	-- switch to modulus
	CASE 	WHEN EXTRACT(MONTH from AEH.dt) IN (1,2,3) THEN 1
			WHEN EXTRACT(MONTH from AEH.dt) IN (4,5,6) THEN 2
			WHEN EXTRACT(MONTH from AEH.dt) IN (7,8,9) THEN 3
			WHEN EXTRACT(MONTH from AEH.dt) IN (10,11,12) THEN 4
			END as q_bin, 
	TIM.period,
	avg(tt_index) AS tt_index_avg,
	percentile_cont(.95) WITHIN GROUP (ORDER BY tt_index) AS tt_index_95

FROM analysis.agg_extract_hour_ah AEH
INNER JOIN ref.timeperiod AS TIM USING (time_15_continuous)
LEFT JOIN ref.holiday AS HOL USING (dt)

WHERE AEH.tt_index IS NOT NULL AND HOL.dt IS NULL AND EXTRACT(DOW FROM AEH.dt) IN (2,3,4)

GROUP BY 	tmc,
		EXTRACT(YEAR FROM AEH.dt),
		TIM.period,
		CASE 	WHEN EXTRACT(MONTH from AEH.dt) IN (1,2,3) THEN 1
				WHEN EXTRACT(MONTH from AEH.dt) IN (4,5,6) THEN 2
				WHEN EXTRACT(MONTH from AEH.dt) IN (7,8,9) THEN 3
				WHEN EXTRACT(MONTH from AEH.dt) IN (10,11,12) THEN 4
				END

ORDER BY 	EXTRACT(YEAR from AEH.dt), 
			CASE 	WHEN EXTRACT(MONTH from AEH.dt) IN (1,2,3) THEN 1
					WHEN EXTRACT(MONTH from AEH.dt) IN (4,5,6) THEN 2
					WHEN EXTRACT(MONTH from AEH.dt) IN (7,8,9) THEN 3
					WHEN EXTRACT(MONTH from AEH.dt) IN (10,11,12) THEN 4
					END, 
			tmc, 
			TIM.period;