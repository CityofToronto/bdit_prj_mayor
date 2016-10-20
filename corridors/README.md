# Corridors
*Reporting congestion trends by corridor*

## Corridor selection
Corridors were selected through local knowledge by selecting TMCs in QGIS and copying them to the table `rdumas.key_corridors`. The names of these corridors can be found in `rdumas.key_corridor_lookup`

## Performance metric aggregation

1. TMC travel times along corridors must first be summed up for every 15-min aggregation using [`sql/corridor_travel_times.sql`](sql/corridor_travel_times.sql) (or the alldata version)
2. Then these are aggregated into monthly median and buffer times (95th - median) with [`sql/monthly_percentiles.sql`](sql/monthly_percentiles.sql)
3. 2014-2016 graphs are plotted in the [`Corridor performance.ipynb`](Corridor performance.ipynb) Jupyter Notebook
4. See [`sql/corridor_Q2oQ2_tt_buff_pct_change.sql`](sql/corridor_Q2oQ2_tt_buff_pct_change.sql) for a query to generate a table of Q2 to Q2 performance changes for the corridors