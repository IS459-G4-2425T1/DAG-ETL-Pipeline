CREATE OR REPLACE VIEW delay_by_day AS
SELECT UniqueCarrier, 
CASE WHEN DayOfWeek = 1 THEN 'Monday' 
WHEN DayOfWeek = 2 THEN 'Tuesday'
WHEN DayOfWeek = 3 THEN 'Wednesday'
WHEN DayOfWeek = 4 THEN 'Thursday'
WHEN DayOfWeek = 5 THEN 'Friday'
WHEN DayOfWeek = 6 THEN 'Saturday'
WHEN DayOfWeek = 7 THEN 'Sunday'
END AS dayofweek, 
ROUND(AVG(arrdelay), 2) AS arrdelay,
ROUND(AVG(depdelay), 2) AS depdelay,
ROUND(AVG(TotalDelay), 2) AS totaldelay
FROM df
GROUP BY UniqueCarrier, DayOfWeek
ORDER BY UniqueCarrier, DayOfWeek;