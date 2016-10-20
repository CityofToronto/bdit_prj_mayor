# Signal Retiming
Before After comparisons of signal retimings on particular corridors.

## Corridor Selection

Based on intersection-intersection descriptions provided in emails. Date ranges for retiming currently hardcoded in the [`Signal Timing performance.ipynb`](Signal Timing performance.ipynb) notebook. Corridors then drawn in QGIS by selecting TMCs. TMC segments don't necessarily line up with retiming start and end points.

## Corridor performance analysis
Since these corridors don't necessarily line up with the key corridors, similar `sql` aggregation has to be performed.

>1. TMC travel times along corridors must first be summed up for every 15-min aggregation using [`sql/signal_timing_travel_times_score30.sql`](sql/signal_timing_travel_times_score30.sql) (or the alldata version)
2. Then these are aggregated into weekly median times with [`sql/signal_timing_weekly.sql`](sql/signal_timing_weekly.sql)

3. [`Signal Timing performance.ipynb`](Signal Timing performance.ipynb) contains code to generate timeseries graphs as well as generate before-after tables for each corridor with 1 month of data.