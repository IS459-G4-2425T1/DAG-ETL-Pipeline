CREATE OR REPLACE VIEW weekly_total_delays AS
SELECT 
    dayofweek,
    SUM(CASE WHEN carrierdelay > 0 THEN 1 ELSE 0 END) AS Carrier_Delay_Count,
    SUM(CASE WHEN weatherdelay > 0 THEN 1 ELSE 0 END) AS Weather_Delay_Count,
    SUM(CASE WHEN nasdelay > 0 THEN 1 ELSE 0 END) AS NAS_Delay_Count,
    SUM(CASE WHEN securitydelay > 0 THEN 1 ELSE 0 END) AS Security_Delay_Count,
    SUM(CASE WHEN lateaircraftdelay > 0 THEN 1 ELSE 0 END) AS Late_Aircraft_Delay_Count,
    SUM(
        CASE WHEN carrierdelay > 0 THEN 1 ELSE 0 END +
        CASE WHEN weatherdelay > 0 THEN 1 ELSE 0 END +
        CASE WHEN nasdelay > 0 THEN 1 ELSE 0 END +
        CASE WHEN securitydelay > 0 THEN 1 ELSE 0 END +
        CASE WHEN lateaircraftdelay > 0 THEN 1 ELSE 0 END
    ) AS Total_No_Delays
FROM 
    df
GROUP BY 
    dayofweek
ORDER BY 
    dayofweek;
