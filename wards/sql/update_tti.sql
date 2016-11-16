UPDATE analysis.agg_extract_hour_alldata AEH SET tt_index = GREATEST(AEH.avg_tt_min / ((ITT.sum_miles+0.0000001)/ITT.speed_overnight*60),1)

FROM (SELECT * FROM gis.inrix_tmc_tor WHERE speed_overnight > 0) ITT

WHERE AEH.tmc = ITT.tmc