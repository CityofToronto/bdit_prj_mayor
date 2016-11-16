TRUNCATE analysis.compare_twoyr;

INSERT INTO analysis.compare_twoyr
SELECT
	MPI.tmc,
	MPI.period,
	SUM(CASE WHEN year_bin = 2014 THEN avg_tt_index ELSE 0 END) AS tti_2014_q2,
	SUM(CASE WHEN year_bin = 2016 THEN avg_tt_index ELSE 0 END) AS tti_2016_q2
	
FROM analysis.mp_index MPI
WHERE q_bin = 2 AND MPI.period IN ('AMPK','PMPK')
GROUP BY MPI.tmc, MPI.period
ORDER BY MPI.tmc, MPI.period;