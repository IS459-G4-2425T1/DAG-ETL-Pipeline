CREATE OR REPLACE VIEW days_seasons_delays AS
SELECT year, month,
dayofmonth, 
CASE WHEN DayOfWeek = 1 THEN 'Monday' 
WHEN DayOfWeek = 2 THEN 'Tuesday'
WHEN DayOfWeek = 3 THEN 'Wednesday'
WHEN DayOfWeek = 4 THEN 'Thursday'
WHEN DayOfWeek = 5 THEN 'Friday'
WHEN DayOfWeek = 6 THEN 'Saturday'
WHEN DayOfWeek = 7 THEN 'Sunday'
END AS dayofweek,
ROUND(AVG(ArrDelay), 2) AS arrdelay, ROUND(AVG(depdelay), 2) AS depdelay, ROUND(AVG(totaldelay), 2) AS totaldelay,
CASE WHEN (month = 1 or month = 2 or month = 12) THEN 'Winter'
WHEN (month = 3 or month = 4 or month = 5) THEN 'Spring'
WHEN (month = 6 or month = 7 or month = 8) THEN 'Summer'
WHEN (month = 9 or month = 10 or month = 11) THEN 'Fall'
END AS season
FROM df
GROUP BY year, month, dayofmonth, dayofweek
ORDER BY year, month, dayofmonth, dayofweek;