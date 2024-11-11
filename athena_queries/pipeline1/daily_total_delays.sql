CREATE OR REPLACE VIEW daily_total_delays AS
SELECT 
    dayofmonth,
    SUM(CASE WHEN carrierdelay > 0 THEN 1 ELSE 0 END) AS Carrier_Delay,
    SUM(CASE WHEN weatherdelay > 0 THEN 1 ELSE 0 END) AS Weather_Delay,
    SUM(CASE WHEN nasdelay > 0 THEN 1 ELSE 0 END) AS NAS_Delay,
    SUM(CASE WHEN securitydelay > 0 THEN 1 ELSE 0 END) AS Security_Delay,
    SUM(CASE WHEN lateaircraftdelay > 0 THEN 1 ELSE 0 END) AS Late_Aircraft_Delay,
    SUM(CASE WHEN carrierdelay > 0 THEN 1 ELSE 0 END) + 
    SUM(CASE WHEN weatherdelay > 0 THEN 1 ELSE 0 END) + 
    SUM(CASE WHEN nasdelay > 0 THEN 1 ELSE 0 END) + 
    SUM(CASE WHEN securitydelay > 0 THEN 1 ELSE 0 END) + 
    SUM(CASE WHEN lateaircraftdelay > 0 THEN 1 ELSE 0 END) AS Total_Delays
FROM 
    pipeline1_airline_data
GROUP BY 
    dayofmonth
ORDER BY 
    dayofmonth;
