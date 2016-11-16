TRUNCATE analysis.ward_summary;

INSERT INTO analysis.ward_summary

SELECT 	TWA.ward, 
	make_date(MPI.year_bin, MPI.q_bin*3-2, 1) AS q_bin, 
	MPI.period, 
	sum(MPI.tt_index_avg * (ITT.sum_miles+0.0000001))/sum(ITT.sum_miles+0.0000001) AS avg_tt_index,
	sum((MPI.tt_index_95 - MPI.tt_index_avg)/MPI.tt_index_avg * (ITT.sum_miles+0.0000001))/sum(ITT.sum_miles+0.0000001) AS avg_buf_index

FROM analysis.mp_index MPI
INNER JOIN ref.tmc_ward TWA USING (tmc)
INNER JOIN gis.inrix_tmc_tor ITT USING (tmc)
WHERE ITT.road_type IS NULL

GROUP BY TWA.ward, make_date(MPI.year_bin, MPI.q_bin*3-2, 1), MPI.period
ORDER BY TWA.ward, make_date(MPI.year_bin, MPI.q_bin*3-2, 1), MPI.period;