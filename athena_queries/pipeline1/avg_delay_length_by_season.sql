CREATE OR REPLACE VIEW avg_delay_length_by_season AS
SELECT 
    season,
    AVG(totaldelay) AS Avg_Total_Delay,
    AVG(carrierdelay) AS Avg_Carrier_Delay,
    AVG(weatherdelay) AS Avg_Weather_Delay,
    AVG(nasdelay) AS Avg_NAS_Delay,
    AVG(securitydelay) AS Avg_Security_Delay,
    AVG(lateaircraftdelay) AS Avg_Late_Aircraft_Delay
FROM 
    df
GROUP BY 
    season
ORDER BY 
    season;
