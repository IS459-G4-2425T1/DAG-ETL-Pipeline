CREATE OR REPLACE VIEW flight_type_delays AS
SELECT
CASE WHEN longhaulflight = 0 THEN 'Short'
WHEN longhaulflight = 1 THEN 'Long'
END AS flightduration, 
UniqueCarrier, scheduledarrhour, scheduleddephour,
ROUND(AVG(ArrDelay), 2) AS arrdelay,
ROUND(AVG(depdelay), 2) AS depdelay,
ROUND(AVG(totaldelay), 2) AS totaldelay
FROM df
GROUP BY UniqueCarrier, ScheduledArrHour, scheduleddephour, longhaulflight;