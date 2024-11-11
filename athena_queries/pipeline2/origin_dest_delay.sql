CREATE OR REPLACE VIEW origin_dest_delay AS
SELECT year, month,
origin, dest, route,
ROUND(AVG(ArrDelay), 2) AS arrdelay, ROUND(AVG(depdelay), 2) AS depdelay, ROUND(AVG(totaldelay), 2) AS totaldelay
FROM df
GROUP BY year, month, origin, dest, route
ORDER BY year, month, origin
;