.tables


SELECT estimated_bod.bod5_g_per_day, wastewater_data.POP, wastewater_data.country
FROM wastewater_data
JOIN estimated_bod
ON estimated_bod.country = wastewater_data.country

SELECT mcf FROM estimated_bod

SELECT wastewater_data., wastewater_data.POP, estimated_bod.bod5_g_per_day