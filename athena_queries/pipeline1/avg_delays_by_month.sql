CREATE OR REPLACE VIEW avg_delays_by_month AS
SELECT 
    month,
    AVG(depdelay) AS Avg_Total_Departure_Delay,
    AVG(carrierdelay) AS Avg_Carrier_Delay,
    AVG(weatherdelay) AS Avg_Weather_Delay,
    AVG(nasdelay) AS Avg_NAS_Delay,
    AVG(securitydelay) AS Avg_Security_Delay,
    AVG(lateaircraftdelay) AS Avg_Late_Aircraft_Delay
FROM 
    pipeline1_airline_data
GROUP BY 
    month
ORDER BY 
    month;
